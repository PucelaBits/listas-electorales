import glob
from collections.abc import Generator

import pymupdf

from common import logger

from .error_fixes import ERROR_FIXERS

_LONG_LINE_THRESHOLD = 150  # Arbitrary threshold for splitting long lines


def _find_column_split_x(page: pymupdf.Page, words: list[str]) -> float:
    """
    Calculates the exact gutter center between two columns using an
    area-weighted average of word boundaries.
    """
    default_mid = page.rect.width / 2

    left_weights = 0.0
    left_x1_sum = 0.0

    right_weights = 0.0
    right_x0_sum = 0.0

    for w in words:
        x0, y0, x1, y1 = w[0], w[1], w[2], w[3]
        width = x1 - x0
        height = y1 - y0
        area = width * height

        # Ignore huge words (like title banners/watermarks) that span across the middle
        if width > page.rect.width * 0.30 and x0 < default_mid < x1:
            continue

        # Classify based on the word's center X coordinate
        word_center_x = (x0 + x1) / 2

        if word_center_x < default_mid:
            left_x1_sum += x1 * area
            left_weights += area
        else:
            right_x0_sum += x0 * area
            right_weights += area

    if left_weights > 0 and right_weights > 0:
        avg_left_x1 = left_x1_sum / left_weights
        avg_right_x0 = right_x0_sum / right_weights

        # The split point is right in the center of the gutter
        if avg_left_x1 < avg_right_x0:
            return (avg_left_x1 + avg_right_x0) / 2

    return default_mid


class PDFReader:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = ERROR_FIXERS.get((region, year, month), None)

    def parse(self) -> Generator[str, None, None]:
        pdf_files = glob.glob(f"{self.folderpath}/candidaturas*.pdf")
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.folderpath}")

        for pdf_path in pdf_files:
            yield from self.__parse_single_file(pdf_path)

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
            for w in page.get_text("words")
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

        # Threshold: if > 15% of the text area is on the right, it's double-column
        ratio = right_column_area / total_area
        result = ratio > 0.15

        if result:
            logger.debug(
                f"Detected double-column layout on page {mid_index} with {right_column_area:.2f}/{total_area:.2f} ({ratio:.2%}) of text area on the right side."
            )
        return result

    def __words_to_text(self, word_list: list, y_tolerance: float = 4.0) -> str:
        """Helper to reconstruct lines of text from floating word coordinates."""
        if not word_list:
            return ""

        # Sort purely top-to-bottom by the exact Y coordinate
        word_list.sort(key=lambda w: w[1])

        lines = []
        curr_line_words = []
        line_anchor_y = None

        for w in word_list:
            y0 = w[1]

            # If it's the first word or within the tolerance of the line's starting Y
            if line_anchor_y is None or abs(y0 - line_anchor_y) <= y_tolerance:
                curr_line_words.append(w)
                if line_anchor_y is None:
                    line_anchor_y = y0
            else:
                # Line is complete. Sort the line's words strictly left-to-right (by X)
                curr_line_words.sort(key=lambda w: w[0])

                # Extract text and add to lines
                lines.append(" ".join(w[4] for w in curr_line_words))

                # Start a new line with the current word
                curr_line_words = [w]
                line_anchor_y = y0

        # Don't forget to process the final line
        if curr_line_words:
            curr_line_words.sort(key=lambda w: w[0])
            lines.append(" ".join(w[4] for w in curr_line_words))

        return "\n".join(lines)

    def __parse_double_column_page(self, page: pymupdf.Page) -> str:
        """Handles text extraction for a two-column layout page."""
        words = page.get_text("words")
        split_x = _find_column_split_x(page, words)

        # Divide words into left and right buckets based on their center points
        left_words = [w for w in words if ((w[0] + w[2]) / 2) < split_x]
        right_words = [w for w in words if ((w[0] + w[2]) / 2) >= split_x]

        # Convert word clusters back into readable paragraph text
        left_text = self.__words_to_text(left_words)
        right_text = self.__words_to_text(right_words)

        return f"{left_text}\n{right_text}"

    def __parse_single_file(self, pdf_path: str) -> Generator[str, None, None]:
        doc = pymupdf.open(pdf_path)
        is_double_col = self.__is_double_column(doc)
        for page in doc:
            if is_double_col:
                text = self.__parse_double_column_page(page)
            else:
                # Standard single-column extraction
                text = page.get_text(sort=True)
            if not text:
                continue

            if self.fix_text is not None:
                text = self.fix_text(text)

            for line in text.split("\n"):
                line = line.strip()
                if not line:
                    continue
                # If the line is too long, it might have multiple stuff inside, split it
                if len(line) > _LONG_LINE_THRESHOLD:
                    # Make a best-effort split using spaces
                    for range_start in range(0, len(line), _LONG_LINE_THRESHOLD):
                        selected_line = line[
                            range_start : range_start + _LONG_LINE_THRESHOLD
                        ].strip()
                        if selected_line:
                            yield selected_line
                else:
                    yield line
