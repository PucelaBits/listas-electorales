from bisect import bisect_right

import pymupdf

from ._internal import (
    deskew_word_boxes,
    estimate_skew_angle,
    filter_words,
    find_optimal_gutter_x,
    words_to_text,
)


def find_min_max_x(words: list[tuple]) -> tuple[float, float]:
    """
    Calculates the min and max x-coordinates of the words on a page.
    """
    if not words:
        return 0.0, 0.0

    x0s, _, x1s, *_ = zip(*words)
    return min(x0s), max(x1s)


def parse_n_column_page(
    page: pymupdf.Page,
    n_columns: int,
    column_splits: list[float] | None = None,
    window_ratio: float = 0.45,
) -> str:
    """
    Handles text extraction for an n-column layout page with OCR skew
    correction and iterative empty-gutter detection.
    """
    if n_columns < 1:
        raise ValueError("n_columns must be at least 1")
    words = page.get_text("words", flags=0)
    words = filter_words(words)
    if not words:
        return ""

    skew_angle = estimate_skew_angle(words)
    if abs(skew_angle) > 0.0001:
        words = deskew_word_boxes(words, skew_angle)
    if n_columns == 1:
        return words_to_text(words)

    if column_splits is not None:
        if len(column_splits) != n_columns - 1:
            raise ValueError(
                f"Length of column_splits ({len(column_splits)}) must be n_columns - 1 ({n_columns - 1})"
            )
        splits = column_splits
    else:
        # For multiple columns, find the optimal gutter positions iteratively
        min_x, max_x = find_min_max_x(words)
        total_width = max_x - min_x
        if total_width <= 0:
            raise ValueError("Invalid word bounding boxes: zero or negative width")
        avg_col_width = total_width / n_columns
        search_radius = avg_col_width * window_ratio
        # Prevents two splits from merging
        min_col_width = avg_col_width * 0.45

        # Iteratively find each of the (n - 1) column gutters left-to-right
        splits = []
        prev_split_x = min_x

        for k in range(1, n_columns):
            nominal_x = min_x + k * avg_col_width

            # Bound search window by both nominal radius and previous split position
            search_min_x = max(
                nominal_x - search_radius,
                prev_split_x + min_col_width,
            )
            # Leave enough room on the right for the remaining (n_columns - k) columns
            max_allowed_x = max_x - (n_columns - k) * min_col_width
            search_max_x = min(nominal_x + search_radius, max_allowed_x)

            split_x = find_optimal_gutter_x(
                words,
                search_min_x=search_min_x,
                search_max_x=search_max_x,
            )
            splits.append(split_x)
            prev_split_x = split_x

    # Partition words into n column buckets
    column_words = [[] for _ in range(n_columns)]
    for w in words:
        mid_x = (w[0] + w[2]) / 2.0
        col_idx = bisect_right(splits, mid_x)
        column_words[col_idx].append(w)
    column_texts = [words_to_text(col) for col in column_words if col]
    return "\n".join(column_texts)


def is_double_column(doc: pymupdf.Document) -> bool:
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
    result = ratio > 0.35

    return result
