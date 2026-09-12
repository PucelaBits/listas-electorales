import glob
import re
from collections import defaultdict
from collections.abc import Generator

import pymupdf

from common import logger

from .parse_fixes import PARSE_FIXES

# Threshold for splitting lines with too many consecutive spaces
_TOO_MANY_SPACES_THRESHOLD = 7

# Pre-compile regex for spaces to handle exact or greater threshold optimally
_MANY_SPACES_REGEX = re.compile(rf" {{{_TOO_MANY_SPACES_THRESHOLD},}}")

# Regex to detect if a string contains any PUA characters in our target range
_PUA_REGEX = re.compile(r"[\uF000-\uF0FF]")

# Pre-computed translation table for C-level string replacement
_PUA_TRANSLATION_TABLE = {i: i - 0xF000 for i in range(0xF000, 0xF100)}


def _fix_mupdf_pua_text(text: str) -> str:
    """
    Shifts characters mapped to the Private Use Area (U+F000 - U+F0FF)
    back to their standard ASCII/Latin-1 Unicode ranges using C-optimized translation.
    """
    return text.translate(_PUA_TRANSLATION_TABLE)


def _find_column_split_x(page: pymupdf.Page, words: list[tuple]) -> float:
    """
    Calculates the center between two columns using the midpoint
    between the leftmost and rightmost text boundaries.
    Ignores headers and footers.
    """
    default_mid = page.rect.width / 2

    # Define vertical limits to ignore headers and footers
    header_limit = page.rect.height * 0.10
    footer_limit = page.rect.height * 0.90

    # Filter out words in header/footer boundaries in a single pass
    valid_words = [w for w in words if header_limit <= w[1] and w[3] <= footer_limit]

    if not valid_words:
        # Fallback to absolute center of the page if no valid text is found
        return default_mid

    # zip(*...) is a highly optimized C-level transpose.
    # x0s = all x0 coords, x1s = all x1 coords.
    x0s, _, x1s, *_ = zip(*valid_words)

    # Use C-level min/max
    return (min(x0s) + max(x1s)) / 2


def _split_too_many_spaces(line: str) -> Generator[str, None, None]:
    """Splits a line into multiple lines if it contains too many consecutive spaces."""
    # Fast initial check using string repetition
    if " " * _TOO_MANY_SPACES_THRESHOLD in line:
        # Use pre-compiled regex for accurate splitting (handles > threshold robustly)
        for segment in _MANY_SPACES_REGEX.split(line):
            segment = segment.strip()
            if segment:
                yield segment
    else:
        yield line


class PDFReader:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = PARSE_FIXES.get((region, year, month), None)

    def parse(self) -> Generator[str, None, None]:
        pdf_files = glob.glob(f"{self.folderpath}/candidaturas*.pdf")
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.folderpath}")

        pdf_files.sort()  # Ensure consistent order
        for pdf_path in pdf_files:
            yield from self.__parse_single_file(pdf_path)

    def __has_pua_text(self, doc: pymupdf.Document) -> bool:
        """
        Scans a sample of the document to determine if it contains Private Use Area (PUA) text.
        Checks the first, middle, and last pages.
        """
        if doc.page_count == 0:
            return False

        # Use a set to avoid checking the same page twice on very short documents
        pages_to_check = {0, doc.page_count // 2, doc.page_count - 1}

        for page_num in pages_to_check:
            text = doc[page_num].get_text("text")
            if _PUA_REGEX.search(text):
                logger.debug(f"Detected PUA encoded text on page {page_num}.")
                return True

        return False

    def __is_double_column(self, doc: pymupdf.Document) -> bool:
        """
        Reads a page in the middle of the document to determine if it uses a two-column layout.
        Returns True if a significant portion of the text area is in the right half,
        ignoring headers and footers.
        """
        if doc.page_count == 0:
            return False

        # Select a page in the middle of the document to avoid title/header pages
        mid_index = doc.page_count // 2
        page = doc[mid_index]

        midpoint_x = page.rect.width / 2
        top_boundary = page.rect.height * 0.10
        bottom_boundary = page.rect.height * 0.90

        # Extract words that fall within the vertical boundaries
        words = [
            w
            for w in page.get_text("words", flags=0)
            if w[1] > top_boundary and w[3] < bottom_boundary
        ]

        if not words:
            return False

        total_area = 0.0
        right_column_area = 0.0

        for w in words:
            # Calculate area: (x1 - x0) * (y1 - y0)
            area = (w[2] - w[0]) * (w[3] - w[1])
            total_area += area

            # If the word starts on the right side, add its area to the right column total
            if w[0] > midpoint_x:
                right_column_area += area

        if total_area == 0:
            return False

        ratio = right_column_area / total_area
        result = ratio > 0.30

        if result:
            logger.debug(
                f"Detected double-column layout on page {mid_index} with {right_column_area:.2f}/{total_area:.2f} ({ratio:.2%}) of text area on the right side."
            )
        return result

    def __words_to_text(
        self, word_list: list, y_tolerance: float = 2.0, needs_pua_fix: bool = False
    ) -> str:
        """Helper to reconstruct lines of text from floating word coordinates."""
        if not word_list:
            return ""

        # Use defaultdict for faster/cleaner grouping by block_no (w[5]) and line_no (w[6])
        grouped_lines = defaultdict(list)
        for w in word_list:
            grouped_lines[(w[5], w[6])].append(w)

        filtered_words = []
        for line_words in grouped_lines.values():
            # Fast transpose to get all coordinates simultaneously
            x0s, y0s, x1s, y1s, texts, *_ = zip(*line_words)

            width = max(max(x1s) - min(x0s), 1)
            height = max(max(y1s) - min(y0s), 1)
            chars_count = sum(len(t) for t in texts)

            # Heuristic: Rotated text has a bounding box that is taller than it is wide.
            # We enforce a chars_count >= 3 to avoid accidentally filtering out
            # naturally narrow horizontal text (like "11" or "il").
            if height > (width * 2.0) and chars_count >= 3:
                continue  # Skip this vertical/rotated line

            filtered_words.extend(line_words)

        if not filtered_words:
            return ""

        # Sort top-to-bottom by the middle Y coordinate
        filtered_words.sort(key=lambda w: (w[1] + w[3]) / 2.0)

        lines = []
        curr_line_words = []
        line_anchor_y = None

        # Pre-resolve the modifier function to avoid branching inside the loop
        clean_text = _fix_mupdf_pua_text if needs_pua_fix else lambda x: x

        for w in filtered_words:
            mid_y = (w[1] + w[3]) / 2.0

            # If it's the first word or within the tolerance of the line's starting Y
            if line_anchor_y is None or abs(mid_y - line_anchor_y) <= y_tolerance:
                curr_line_words.append(w)
                if line_anchor_y is None:
                    line_anchor_y = mid_y
            else:
                # Line is complete. Sort the line's words strictly left-to-right (by X)
                curr_line_words.sort(key=lambda x: x[0])
                lines.append(" ".join(clean_text(x[4]) for x in curr_line_words))

                # Start a new line with the current word
                curr_line_words = [w]
                line_anchor_y = mid_y

        # Don't forget to process the final line
        if curr_line_words:
            curr_line_words.sort(key=lambda x: x[0])
            lines.append(" ".join(clean_text(x[4]) for x in curr_line_words))

        return "\n".join(lines)

    def __parse_double_column_page(
        self, page: pymupdf.Page, needs_pua_fix: bool
    ) -> str:
        """Handles text extraction for a two-column layout page."""
        words = page.get_text("words", flags=0)
        split_x = _find_column_split_x(page, words)

        left_words = []
        right_words = []

        # Single pass to partition words to left/right halves
        for w in words:
            if (w[0] + w[2]) / 2.0 < split_x:
                left_words.append(w)
            else:
                right_words.append(w)

        left_text = self.__words_to_text(left_words, needs_pua_fix=needs_pua_fix)
        right_text = self.__words_to_text(right_words, needs_pua_fix=needs_pua_fix)

        return f"{left_text}\n{right_text}"

    def __parse_single_file(self, pdf_path: str) -> Generator[str, None, None]:
        doc = pymupdf.open(pdf_path)
        is_double_col = self.__is_double_column(doc)
        needs_pua_fix = self.__has_pua_text(doc)

        for page in doc:
            if is_double_col:
                text = self.__parse_double_column_page(page, needs_pua_fix)
            else:
                text = self.__words_to_text(
                    page.get_text("words", flags=0), needs_pua_fix=needs_pua_fix
                )

            if not text:
                continue

            if self.fix_text is not None:
                text = self.fix_text(text)

            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                yield from _split_too_many_spaces(line)
