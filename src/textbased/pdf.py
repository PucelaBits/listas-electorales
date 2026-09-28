import glob
import math
import re
from collections import defaultdict
from collections.abc import Generator
from statistics import median

import pymupdf

from common import logger

from .parse_fixes import PARSE_FIXES

# TODO: Check if encoding is correct

# Threshold for splitting lines with too many consecutive spaces
_TOO_MANY_SPACES_THRESHOLD = 7

# Pre-compile regex for spaces to handle exact or greater threshold optimally
_MANY_SPACES_REGEX = re.compile(rf" {{{_TOO_MANY_SPACES_THRESHOLD},}}")

HARCODED_COLUMN_FIX = {
    ("cataluna", 1988, 5): 3,
    ("cataluna", 1992, 3): 3,
    ("cataluna", 1995, 11): 3,
    ("castilla_la_mancha", 1999, 6): 1,
    ("cataluna", 1999, 10): 3,
    ("murcia", 2003, 5): 2,
    ("cataluna", 2003, 11): 3,
    ("cataluna", 2006, 11): 3,
    ("castilla_la_mancha", 2007, 5): 3,
    ("cantabria", 2011, 5): 1,
    ("canarias", 2015, 5): 1,
}


def _find_min_max_x(words: list[tuple]) -> float:
    """
    Calculates the min and max x-coordinates of the words on a page.
    """
    # zip(*...) is a highly optimized C-level transpose.
    # x0s = all x0 coords, x1s = all x1 coords.
    x0s, _, x1s, *_ = zip(*words)

    return min(x0s), max(x1s)


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


def _estimate_skew_angle(words: list, max_angle_deg: float = 15.0) -> float:
    """
    Estimates the page skew angle (in radians) using the median slope
    between horizontally adjacent word boxes.
    """
    if len(words) < 2:
        return 0.0

    # Sort left-to-right by x0
    sorted_x = sorted(words, key=lambda w: w[0])
    angles = []
    max_rad = math.radians(max_angle_deg)

    for i, w1 in enumerate(sorted_x):
        x0_1, y0_1, x1_1, y1_1, _, _, h1 = w1
        cy1 = (y0_1 + y1_1) / 2.0

        # Look ahead at nearby words to the right
        for j in range(i + 1, min(i + 15, len(sorted_x))):
            w2 = sorted_x[j]
            x0_2, y0_2, x1_2, y1_2, _, _, h2 = w2

            dx = x0_2 - x1_1  # Horizontal gap between word1 right and word2 left
            if dx < 0:
                continue
            if dx > max(h1, h2) * 4.0:
                break  # Too far apart horizontally to be an immediate neighbor

            cy2 = (y0_2 + y1_2) / 2.0
            dy = cy2 - cy1

            # Check if roughly on the same line and similar font size
            if abs(dy) <= max(h1, h2) * 0.8 and (0.5 <= h1 / h2 <= 2.0):
                # Measure center-to-center angle
                center_dx = ((x0_2 + x1_2) - (x0_1 + x1_1)) / 2.0
                if center_dx > 0:
                    angle = math.atan2(dy, center_dx)
                    if abs(angle) <= max_rad:
                        angles.append(angle)
                break  # Match only the closest valid right-hand neighbor

    return median(angles) if angles else 0.0

class PDFReader:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = PARSE_FIXES.get((region, year, month), None)
        self.column_count = HARCODED_COLUMN_FIX.get((region, year, month), None)

    def parse(self) -> Generator[str, None, None]:
        pdf_files = glob.glob(f"{self.folderpath}/candidaturas*.pdf")
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.folderpath}")

        pdf_files.sort()  # Ensure consistent order
        for pdf_path in pdf_files:
            yield from self.__parse_single_file(pdf_path)

    def __is_double_column(self, doc: pymupdf.Document, force_page: int = None) -> bool:
        """
        Reads a page in the middle of the document to determine if it uses a two-column layout.
        Returns True if a significant portion of the text area is in the right half,
        ignoring headers and footers.
        """
        if doc.page_count == 0:
            return False

        # If a specific page is forced, use it
        if force_page is not None:
            mid_index = force_page
        else:
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
        result = ratio > 0.35

        return result

    def __words_to_text(self, word_list: list, overlap_ratio: float = 0.5) -> str:
        """
        Reconstructs lines of text strictly from OCR word coordinates (x0, y0, x1, y1, text),
        handling page skew, local curvature, and varying font sizes.
        """
        if not word_list:
            return ""

        # 1. Filter out vertical/rotated words using only bounding box + text
        filtered_words = []
        for w in word_list:
            x0, y0, x1, y1, text = w[0], w[1], w[2], w[3], str(w[4]).strip()
            if not text:
                continue

            width = max(x1 - x0, 1e-3)
            height = max(y1 - y0, 1e-3)

            # Skip vertical text (taller than wide with >= 3 characters)
            if height > (width * 2.0) and len(text) >= 3:
                continue

            filtered_words.append((x0, y0, x1, y1, text, width, height))

        if not filtered_words:
            return ""

        # 2. Estimate global page skew angle from adjacent word pairs
        skew_angle = _estimate_skew_angle(filtered_words)
        cos_a = math.cos(skew_angle)
        sin_a = math.sin(skew_angle)

        # 3. Project each word into deskewed coordinates
        # Rotating by -skew_angle makes tilted horizontal lines flat:
        # y_deskewed = cy * cos(theta) - cx * sin(theta)
        deskewed_words = []
        for x0, y0, x1, y1, text, width, height in filtered_words:
            cx = (x0 + x1) / 2.0
            cy = (y0 + y1) / 2.0
            rx = cx * cos_a + cy * sin_a
            ry = cy * cos_a - cx * sin_a
            deskewed_words.append({
                "x0": x0,
                "rx": rx,
                "ry": ry,
                "ry0": ry - height / 2.0,
                "ry1": ry + height / 2.0,
                "height": height,
                "text": text,
            })

        # 4. Sort top-to-bottom by deskewed Y
        deskewed_words.sort(key=lambda w: w["ry"])

        # 5. Cluster into lines using height-proportional tolerance & running anchor
        lines = []
        curr_line = [deskewed_words[0]]
        running_ry = deskewed_words[0]["ry"]
        running_h = deskewed_words[0]["height"]

        for w in deskewed_words[1:]:
            # Dynamic threshold scales automatically with font height
            max_dy = min(running_h, w["height"]) * overlap_ratio

            if abs(w["ry"] - running_ry) <= max_dy:
                curr_line.append(w)
                # Exponential moving average tracks subtle local page curl/warp
                running_ry = 0.7 * running_ry + 0.3 * w["ry"]
                running_h = 0.7 * running_h + 0.3 * w["height"]
            else:
                curr_line.sort(key=lambda item: item["rx"])
                lines.append(" ".join(item["text"] for item in curr_line))

                curr_line = [w]
                running_ry = w["ry"]
                running_h = w["height"]

        if curr_line:
            curr_line.sort(key=lambda item: item["rx"])
            lines.append(" ".join(item["text"] for item in curr_line))

        return "\n".join(lines)

    def __parse_single_column_page(self, page: pymupdf.Page) -> str:
        """Handles text extraction for a single-column layout page."""
        words = page.get_text("words", flags=0)
        return self.__words_to_text(words)

    def __parse_double_column_page(self, page: pymupdf.Page) -> str:
        """Handles text extraction for a two-column layout page."""
        words = page.get_text("words", flags=0)
        # split_x = _find_column_split_x(words)
        split_x = page.rect.width / 2

        left_words = []
        right_words = []

        # Single pass to partition words to left/right halves
        for w in words:
            if (w[0] + w[2]) / 2.0 < split_x:
                left_words.append(w)
            else:
                right_words.append(w)

        left_text = self.__words_to_text(left_words)
        right_text = self.__words_to_text(right_words)

        return f"{left_text}\n{right_text}"

    def __parse_triple_column_page(self, page: pymupdf.Page) -> str:
        """Handles text extraction for a three-column layout page."""
        words = page.get_text("words", flags=0)
        min_x, max_x = _find_min_max_x(words)
        split_x1 = min_x + (max_x - min_x) / 3
        split_x2 = min_x + 2 * (max_x - min_x) / 3

        left_words = []
        middle_words = []
        right_words = []

        # Single pass to partition words into three columns
        for w in words:
            mid_x = (w[0] + w[2]) / 2.0
            if mid_x < split_x1:
                left_words.append(w)
            elif mid_x < split_x2:
                middle_words.append(w)
            else:
                right_words.append(w)

        left_text = self.__words_to_text(left_words)
        middle_text = self.__words_to_text(middle_words)
        right_text = self.__words_to_text(right_words)

        return f"{left_text}\n{middle_text}\n{right_text}"

    def __parse_single_file(self, pdf_path: str) -> Generator[str, None, None]:
        doc = pymupdf.open(pdf_path)
        if self.column_count is None:
            if self.__is_double_column(doc):
                logger.debug(
                    f"Detected double-column layout in {pdf_path}. Using double-column parsing."
                )
                parse_method = self.__parse_double_column_page
            else:
                logger.debug(
                    f"Detected single-column layout in {pdf_path}. Using single-column parsing."
                )
                parse_method = self.__parse_single_column_page
        elif self.column_count == 3:
            logger.debug(
                f"Using hardcoded triple-column layout for {pdf_path}. Using triple-column parsing."
            )
            parse_method = self.__parse_triple_column_page
        elif self.column_count == 2:
            logger.debug(
                f"Using hardcoded double-column layout for {pdf_path}. Using double-column parsing."
            )
            parse_method = self.__parse_double_column_page
        else:
            logger.debug(
                f"Using hardcoded single-column layout for {pdf_path}. Using single-column parsing."
            )
            parse_method = self.__parse_single_column_page

        for page in doc:
            text = parse_method(page)

            if not text:
                continue

            if self.fix_text is not None:
                text = self.fix_text(text)

            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                yield from _split_too_many_spaces(line)
