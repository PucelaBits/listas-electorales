import glob
import re
from collections.abc import Generator

import pymupdf

from common import logger

from .error_fixes import ERROR_FIXERS

# Threshold for splitting lines with too many consecutive spaces
_TOO_MANY_SPACES_THRESHOLD = 7

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
    page_height = page.rect.height

    # Define vertical limits to ignore headers and footers
    header_limit = page_height * 0.10
    footer_limit = page_height * 0.90

    min_x = float("inf")
    max_x = float("-inf")

    for w in words:
        x0, y0, x1, y1 = w[0], w[1], w[2], w[3]

        # Skip words in the header or footer regions
        if y1 < header_limit or y0 > footer_limit:
            continue

        # Track the absolute minimum x and maximum x
        min_x = min(min_x, x0)
        max_x = max(max_x, x1)

    # If we found valid text boundaries, return their midpoint
    if min_x != float("inf") and max_x != float("-inf"):
        return (min_x + max_x) / 2

    # Fallback to absolute center of the page if no valid text is found
    return default_mid


def _split_too_many_spaces(
    line: str, space_threshold: int = _TOO_MANY_SPACES_THRESHOLD
) -> Generator[str, None, None]:
    """Splits a line into multiple lines if it contains too many consecutive spaces."""
    if " " * space_threshold in line:
        for segment in line.split(" " * space_threshold):
            segment = segment.strip()
            if segment:
                yield segment
    else:
        yield line


class PDFReader:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = ERROR_FIXERS.get((region, year, month), None)

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

        # Define vertical boundaries (ignore top 10% and bottom 10%)
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

        # Ignore vertical or rotated text
        grouped_lines = {}
        for w in word_list:
            # w[5] is block_no, w[6] is line_no
            key = (w[5], w[6])
            grouped_lines.setdefault(key, []).append(w)

        filtered_words = []
        for line_words in grouped_lines.values():
            # Calculate the bounding box for the entire line
            min_x = min(w[0] for w in line_words)
            min_y = min(w[1] for w in line_words)
            max_x = max(w[2] for w in line_words)
            max_y = max(w[3] for w in line_words)

            # Avoid division by zero
            width = max(max_x - min_x, 1)
            height = max(max_y - min_y, 1)
            chars_count = sum(len(w[4]) for w in line_words)

            # Heuristic: Rotated text has a bounding box that is taller than it is wide.
            # We enforce a chars_count >= 3 to avoid accidentally filtering out
            # naturally narrow horizontal text (like "11" or "il").
            if height > (width * 2.0) and chars_count >= 3:
                continue  # Skip this vertical/rotated line

            filtered_words.extend(line_words)

        word_list = filtered_words

        if not word_list:
            return ""

        # Sort top-to-bottom by the middle Y coordinate
        word_list.sort(key=lambda w: (w[1] + w[3]) / 2.0)

        lines = []
        curr_line_words = []
        line_anchor_y = None

        for w in word_list:
            # Calculate the vertical center of the current word
            mid_y = (w[1] + w[3]) / 2.0

            # If it's the first word or within the tolerance of the line's starting Y
            if line_anchor_y is None or abs(mid_y - line_anchor_y) <= y_tolerance:
                curr_line_words.append(w)
                if line_anchor_y is None:
                    line_anchor_y = mid_y
            else:
                # Line is complete. Sort the line's words strictly left-to-right (by X)
                curr_line_words.sort(key=lambda w: w[0])

                if needs_pua_fix:
                    lines.append(
                        " ".join(_fix_mupdf_pua_text(w[4]) for w in curr_line_words)
                    )
                else:
                    lines.append(" ".join(w[4] for w in curr_line_words))

                # Start a new line with the current word
                curr_line_words = [w]
                line_anchor_y = mid_y

        # Don't forget to process the final line
        if curr_line_words:
            curr_line_words.sort(key=lambda w: w[0])
            if needs_pua_fix:
                lines.append(
                    " ".join(_fix_mupdf_pua_text(w[4]) for w in curr_line_words)
                )
            else:
                lines.append(" ".join(w[4] for w in curr_line_words))

        return "\n".join(lines)

    def __parse_double_column_page(
        self, page: pymupdf.Page, needs_pua_fix: bool
    ) -> str:
        """Handles text extraction for a two-column layout page."""
        words = page.get_text("words", flags=0)
        split_x = _find_column_split_x(page, words)

        # Divide words into left and right buckets based on their center points
        left_words = [w for w in words if ((w[0] + w[2]) / 2) < split_x]
        right_words = [w for w in words if ((w[0] + w[2]) / 2) >= split_x]

        # Convert word clusters back into readable paragraph text
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
