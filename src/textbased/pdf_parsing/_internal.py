import math
from bisect import bisect_left
from statistics import median


def estimate_skew_angle(words: list, max_angle_deg: float = 15.0) -> float:
    """
    Estimates the page skew angle (in radians) using the median slope
    between horizontally adjacent word boxes, using only bbox coords & height.
    """
    if len(words) < 2:
        return 0.0

    # Sort left-to-right by x0 and pre-extract x0 keys for binary search
    sorted_x = sorted(words, key=lambda w: w[0])
    x0_keys = [w[0] for w in sorted_x]
    angles = []
    max_rad = math.radians(max_angle_deg)

    for i, w1 in enumerate(sorted_x):
        x0_1, y0_1, x1_1, y1_1 = w1[0], w1[1], w1[2], w1[3]
        h1 = y1_1 - y0_1
        if h1 <= 0:
            continue
        cy1 = (y0_1 + y1_1) / 2.0

        # Jump directly to the first word whose left edge (x0_2) >= w1's right edge (x1_1)
        start_j = bisect_left(x0_keys, x1_1, lo=i + 1)

        for j in range(start_j, len(sorted_x)):
            w2 = sorted_x[j]
            x0_2, y0_2, x1_2, y1_2 = w2[0], w2[1], w2[2], w2[3]
            h2 = y1_2 - y0_2
            if h2 <= 0:
                continue

            dx = x0_2 - x1_1  # Guaranteed >= 0 due to bisect_left
            if dx > h1 * 4.0:
                break  # All subsequent words in sorted_x are even further right

            cy2 = (y0_2 + y1_2) / 2.0
            dy = cy2 - cy1

            # Check if roughly on the same line and similar font size
            if abs(dy) <= max(h1, h2) * 0.8 and (0.5 <= h1 / h2 <= 2.0):
                center_dx = ((x0_2 + x1_2) - (x0_1 + x1_1)) / 2.0
                if center_dx > 0:
                    angle = math.atan2(dy, center_dx)
                    if abs(angle) <= max_rad:
                        angles.append(angle)
                break  # Match only the closest valid right-hand neighbor

    return median(angles) if angles else 0.0


def deskew_word_boxes(word_list: list[tuple], skew_angle: float) -> list[tuple]:
    """
    Projects word centers by -skew_angle while preserving original width and height.
    """
    cos_a = math.cos(skew_angle)
    sin_a = math.sin(skew_angle)

    deskewed = []
    for w in word_list:
        x0, y0, x1, y1, text = w[0], w[1], w[2], w[3], w[4]
        width = w[5] if len(w) == 7 else max(x1 - x0, 1e-3)
        height = w[6] if len(w) == 7 else max(y1 - y0, 1e-3)

        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        rx = cx * cos_a + cy * sin_a
        ry = cy * cos_a - cx * sin_a

        # Reconstruct box around deskewed center (rx, ry) with original dimensions
        deskewed.append(
            (
                rx - width / 2.0,  # rx0
                ry - height / 2.0,  # ry0
                rx + width / 2.0,  # rx1
                ry + height / 2.0,  # ry1
                text,
                width,
                height,
            )
        )

    return deskewed


def _filter_body_spans(
    words: list,
    search_min_x: float,
    search_max_x: float,
    margin_ratio: float,
    max_height_ratio: float,
) -> list[tuple[float, float, float]]:
    """
    Filters word boxes down to body-column words, removing running headers/footers,
    large-font headings, and full-width or centered spanning lines.
    Returns a list of (x0, x1, height) tuples.
    """
    if not words:
        return []

    # 1. Vertical margin cut: ignore running headers and footers
    min_y = min(w[1] for w in words)
    max_y = max(w[3] for w in words)
    page_h = max_y - min_y
    top_cut = min_y + page_h * margin_ratio
    bottom_cut = max_y - page_h * margin_ratio

    # 2. Font-height cut: estimate body font height via median
    heights = [max(1.0, w[3] - w[1]) for w in words]
    median_h = median(heights)
    min_body_h = median_h * 0.50
    max_body_h = median_h * max_height_ratio

    body_candidates = [
        w
        for w in words
        if (w[1] >= top_cut and w[3] <= bottom_cut)
        and (min_body_h <= (w[3] - w[1]) <= max_body_h)
    ]

    # Fallback if the page only has a few lines of text
    if len(body_candidates) < 5:
        body_candidates = list(words)

    # 3. Group into approximate horizontal lines to drop centered/spanning headers
    sorted_by_y = sorted(body_candidates, key=lambda w: (w[1] + w[3]) / 2.0)
    lines: list[list[tuple]] = []
    for w in sorted_by_y:
        cy = (w[1] + w[3]) / 2.0
        if not lines:
            lines.append([w])
            continue
        prev_cy = (lines[-1][-1][1] + lines[-1][-1][3]) / 2.0
        if abs(cy - prev_cy) <= median_h * 0.6:
            lines[-1].append(w)
        else:
            lines.append([w])

    # Keep only lines that don't bridge continuously across the central gutter zone
    window_w = search_max_x - search_min_x
    core_min_x = search_min_x + window_w * 0.25
    core_max_x = search_max_x - window_w * 0.25
    max_word_space = median_h * 1.8  # Normal space between words in a single line

    filtered_spans: list[tuple[float, float, float]] = []
    for line in lines:
        line.sort(key=lambda w: w[0])

        # Check if this line crosses the core window
        line_x0 = line[0][0]
        line_x1 = max(w[2] for w in line)
        crosses_core = line_x0 < core_max_x and line_x1 > core_min_x
        if crosses_core and len(line) > 1:
            # Find any horizontal gap between adjacent words that overlaps the search window
            gaps_overlapping_window = [
                line[i + 1][0] - line[i][2]
                for i in range(len(line) - 1)
                if line[i][2] < search_max_x and line[i + 1][0] > search_min_x
            ]
            max_gap = max(gaps_overlapping_window, default=0.0)
            # If words march right through the window with only normal word spacing,
            # it is a spanning title, caption, or centered header -> skip the line
            if gaps_overlapping_window and max_gap <= max_word_space:
                continue

        for w in line:
            filtered_spans.append((w[0], w[2], max(1.0, w[3] - w[1])))

    # Final safety fallback if every line was filtered out
    if not filtered_spans:
        return [(w[0], w[2], max(1.0, w[3] - w[1])) for w in body_candidates]

    return filtered_spans


def find_optimal_gutter_x(
    words: list,
    search_min_x: float,
    search_max_x: float,
    step: float = 1.5,
    margin_ratio: float = 0.05,
    max_height_ratio: float = 1.35,
) -> float:
    """
    Iteratively searches [search_min_x, search_max_x] for the vertical line x
    that crosses as few body words as possible and sits in the widest empty corridor,
    ignoring headers, footers, titles, and spanning lines.
    """
    if search_max_x <= search_min_x or not words:
        return (search_min_x + search_max_x) / 2.0

    # Pre-extract filtered (x0, x1, height) spans for body text only
    spans = _filter_body_spans(
        words,
        search_min_x=search_min_x,
        search_max_x=search_max_x,
        margin_ratio=margin_ratio,
        max_height_ratio=max_height_ratio,
    )

    page_min_x = min((s[0] for s in spans), default=search_min_x)
    page_max_x = max((s[1] for s in spans), default=search_max_x)

    # Build candidate x positions on uniform grid
    candidates = []
    curr_x = search_min_x
    while curr_x <= search_max_x:
        candidates.append(curr_x)
        curr_x += step

    best_x = (search_min_x + search_max_x) / 2.0
    min_cost = float("inf")
    max_clearance = -1.0

    for x in candidates:
        cost = 0.0
        nearest_left_edge = page_min_x
        nearest_right_edge = page_max_x

        for x0, x1, h in spans:
            if x0 < x < x1:
                # Word is crossed: penalize by how deeply the line cuts into the word
                penetration = min(x - x0, x1 - x)
                cost += penetration * h
            elif x1 <= x:
                nearest_left_edge = max(nearest_left_edge, x1)
            elif x0 >= x:
                nearest_right_edge = min(nearest_right_edge, x0)

        # Clearance is the width of the empty corridor around x,
        # favoring lines centered within that corridor
        left_gap = max(0.0, x - nearest_left_edge)
        right_gap = max(0.0, nearest_right_edge - x)
        clearance = (left_gap + right_gap) + min(left_gap, right_gap)

        # Prefer lower intersection cost; break ties using the widest empty corridor
        if cost < min_cost - 1e-3 or (
            abs(cost - min_cost) <= 1e-3 and clearance > max_clearance
        ):
            min_cost = cost
            max_clearance = clearance
            best_x = x

    return best_x


def filter_words(word_list: list[tuple]) -> list[tuple]:
    """
    Filters out empty and vertical/rotated words from PyMuPDF word tuples,
    normalizing each tuple to (x0, y0, x1, y1, text, width, height).
    """
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
    return filtered_words


def words_to_text(word_list: list[tuple], overlap_ratio: float = 0.5) -> str:
    """
    Reconstructs lines of text strictly from OCR word coordinates (x0, y0, x1, y1, text, ...),
    handling page skew, local curvature, and varying font sizes.
    """
    if not word_list:
        return ""

    # 1. Sort top-to-bottom by deskewed vertical center (ry)
    word_list = sorted(word_list, key=lambda w: (w[1] + w[3]) / 2.0)

    # 2. Cluster into lines using height-proportional tolerance & running anchor
    first = word_list[0]
    lines: list[str] = []
    curr_line: list[tuple] = [first]
    running_ry = (first[1] + first[3]) / 2.0
    # Only use w[6] if tuple is our normalized 7-tuple (not PyMuPDF's 8-tuple)
    running_h = first[6] if len(first) == 7 else max(first[3] - first[1], 1e-3)

    for w in word_list[1:]:
        w_ry = (w[1] + w[3]) / 2.0
        w_h = w[6] if len(w) == 7 else max(w[3] - w[1], 1e-3)

        # Dynamic threshold scales automatically with font height
        max_dy = min(running_h, w_h) * overlap_ratio

        if abs(w_ry - running_ry) <= max_dy:
            curr_line.append(w)
            # Exponential moving average tracks subtle local page curl/warp
            running_ry = 0.7 * running_ry + 0.3 * w_ry
            running_h = 0.7 * running_h + 0.3 * w_h
        else:
            # Sort by horizontal center (rx) to match original implementation
            curr_line.sort(key=lambda item: (item[0] + item[2]) / 2.0)
            lines.append(" ".join(item[4] for item in curr_line))

            curr_line = [w]
            running_ry = w_ry
            running_h = w_h

    if curr_line:
        curr_line.sort(key=lambda item: (item[0] + item[2]) / 2.0)
        lines.append(" ".join(item[4] for item in curr_line))

    return "\n".join(lines)
