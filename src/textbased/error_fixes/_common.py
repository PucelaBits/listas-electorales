import re
from collections.abc import Callable

ERROR_FIXERS: dict[tuple[str, int, int], Callable[[str], str]] = {}


def register_fixer(region: str, year: int, month: int):
    """Decorator to register a text-fixing function for a specific batch."""

    def decorator(func: Callable[[str], str]):
        ERROR_FIXERS[(region, year, month)] = func
        return func

    return decorator


def clean_ocr_numbers(text: str) -> str:
    """Cleans up common OCR errors in the text, such as stray punctuation, missing dots after numbers, and inconsistent formatting."""
    # Replace common OCR misreads of numbers
    text = text.replace("1O", "10")
    text = text.replace("I0", "10")
    text = text.replace("T0", "10")
    text = text.replace("lO", "10")
    text = text.replace("l1", "11")
    text = text.replace("1l", "11")
    text = text.replace("1T", "11")
    text = text.replace("l2", "12")
    text = text.replace("l3", "13")
    text = text.replace("l4", "14")
    text = text.replace("l5", "15")
    text = text.replace("l6", "16")
    text = text.replace("l7", "17")
    text = text.replace("l8", "18")
    text = text.replace("l9", "19")
    # This could be dangerous, that's why we require the dot at the end
    text = text.replace("ll.", "11.")
    text = text.replace("IO.", "10.")
    text = text.replace("l.", "1.")
    text = text.replace("S.", "5.")
    # Clean up "Núm" variations (e.g., "Núm.-", "Núm.- ", "Núm ")
    text = re.sub(r"Núm[\.\-\s]+", "Núm. ", text)
    # Replaces the N2 {number} with Núm. {number}
    text = re.sub(r"N(?:\.2|\ 2|[2\.])[\s-]+(\d+)", r"\1", text)

    # Remove stray quotes around numbers and dots
    text = re.sub(r"['´`\"](?=\d)", "", text)
    text = re.sub(r"(?<=\d)['´`\"]", "", text)
    text = re.sub(r"(?<=\d\.)['´`\"]", "", text)

    # Fix SINGLE colons and exclamation marks after numbers (e.g., "11:" -> "11.")
    text = re.sub(r"\b(\d+)[:!•]", r"\1.", text)

    # Fix spaces between the number and the dot (e.g., "11 . " -> "11. ")
    text = re.sub(r"\b(\d+)\s*\.\s*", r"\1. ", text)

    # Fix CLUSTERS of messy punctuation (dots, dashes, commas, colons, exclamation marks)
    text = re.sub(r"\b(\d+)\s*[\.\-\,:\!•'·;]{2,}\s*", r"\1. ", text)

    # Fix stray dots before list numbers (e.g., ".13." -> "13.")
    text = re.sub(re.compile(r"^\ *[\.,-]\ *(\d+)\ *[\.,]", re.MULTILINE), r"\1.", text)
    # Add missing dots after numbers preceding names/entities (e.g., "10 Don" -> "10. Don")
    text = re.sub(r"\b(\d+)\ *(?=Don|Doña|[A-Z]{2,})", r"\1. ", text)

    # Fix commas separating titles (e.g., "Don,Juan" -> "Don Juan")
    text = re.sub(r"(Don|Doña)[,|-]", r"\1 ", text)

    # Remove stray single letters surrounded by dots after numbers (e.g., "3.x. " -> "3. ")
    text = re.sub(r"\b(\d+)\.[a-zA-Z]\.\s*", r"\1. ", text)

    return text


_HAS_NUMBER_RE = re.compile(r"^(\d+)\.")


def autofill_missing_numbers(text: str) -> str:
    """
    Automatically fills in missing numbers in a list of candidates.
    It look at the line before and after without a number to determine the missing number.
    """
    lines = text.splitlines()
    for i in range(1, len(lines) - 1):
        if not _HAS_NUMBER_RE.match(lines[i]):
            prev_match = _HAS_NUMBER_RE.match(lines[i - 1])
            next_match = _HAS_NUMBER_RE.match(lines[i + 1])
            if prev_match and next_match:
                prev_number = int(prev_match.group(1))
                next_number = int(next_match.group(1))
                if next_number - prev_number == 2:
                    missing_number = prev_number + 1
                    lines[i] = f"{missing_number}. {lines[i].lstrip()}"
    text = "\n".join(lines)
    return text


def fill_missing_numbers(
    text: str, start_line: str, end_line: str, start_number: int = 1
) -> str:
    """
    Fill missing numbers between start_line and end_line without splitting the whole text.
    """
    start_pattern = re.compile(rf"^{re.escape(start_line)}\r?$", re.MULTILINE)
    end_pattern = re.compile(rf"^{re.escape(end_line)}\r?$", re.MULTILINE)

    start_match = start_pattern.search(text)
    end_match = end_pattern.search(text)

    if not start_match:
        raise ValueError("start_line not found in the text.")

    if not end_match:
        raise ValueError("end_line not found in the text.")

    start_pos = start_match.start()
    end_pos = end_match.end()

    if start_pos > end_match.start():
        raise ValueError("Unexpected order of start_line and end_line in the text.")

    block = text[start_pos:end_pos]

    block_lines = block.splitlines(keepends=True)

    for i, line in enumerate(block_lines):
        match = _HAS_NUMBER_RE.match(line)
        if match:
            # Replace the number with the current start_number
            block_lines[i] = block_lines[i].replace(
                match.group(1), str(start_number), 1
            )
        else:
            block_lines[i] = f"{start_number}. {line}"
        start_number += 1

    return text[:start_pos] + "".join(block_lines) + text[end_pos:]


_TEN_LINE_OCR_RE = re.compile(
    r"^(?P<L1>[^\d\n].*?)\r?\n"
    r"(?P<L2>[^\d\n].*?)\r?\n"
    r"(?P<L3>[^\d\n].*?)\r?\n"
    r"(?P<L4>[^\d\n].*?)\r?\n"
    r"(?P<L5>[^\d\n].*?)\r?\n"
    r"(?P<L6>[^\d\n].*?)\r?\n"
    r"(?P<L7>[^\d\n].*?)\r?\n"
    r"(?P<L8>[^\d\n].*?)\r?\n"
    r"(?P<L9>[^\d\n].*?)\r?\n"
    r"(?P<L10>10\..*?)$",
    re.MULTILINE,
)


def fix_ten_line_ocr(text: str) -> str:
    # Match 9 lines that don't start with a digit, followed by the 10th line
    # Replace using the captured groups and prepending the numbers
    return _TEN_LINE_OCR_RE.sub(
        (
            r"1. \g<L1>\n"
            r"2. \g<L2>\n"
            r"3. \g<L3>\n"
            r"4. \g<L4>\n"
            r"5. \g<L5>\n"
            r"6. \g<L6>\n"
            r"7. \g<L7>\n"
            r"8. \g<L8>\n"
            r"9. \g<L9>\n"
            r"\g<L10>"
        ),
        text,
    )


_NINE_LINE_OCR_RE = re.compile(
    r"^(?P<L1>[^\d\n].*?)\r?\n"
    r"(?P<L2>[^\d\n].*?)\r?\n"
    r"(?P<L3>[^\d\n].*?)\r?\n"
    r"(?P<L4>[^\d\n].*?)\r?\n"
    r"(?P<L5>[^\d\n].*?)\r?\n"
    r"(?P<L6>[^\d\n].*?)\r?\n"
    r"(?P<L7>[^\d\n].*?)\r?\n"
    r"(?P<L8>[^\d\n].*?)\r?\n"
    r"(?P<L9>9\..*?)$",
    re.MULTILINE,
)


def fix_nine_line_ocr(text: str) -> str:
    # Match 8 lines that don't start with a digit, followed by the 9th line
    return _NINE_LINE_OCR_RE.sub(
        (
            r"1. \g<L1>\n"
            r"2. \g<L2>\n"
            r"3. \g<L3>\n"
            r"4. \g<L4>\n"
            r"5. \g<L5>\n"
            r"6. \g<L6>\n"
            r"7. \g<L7>\n"
            r"8. \g<L8>\n"
            r"\g<L9>"
        ),
        text,
    )


def remove_single_letter_lines(text: str) -> str:
    """
    Removes lines that consist of a single letter (A-Z, a-z) or multiple single
    letters separated by spaces, optionally followed by dots.
    """
    pattern = r"^[ \t]*[A-Za-z]\.?(?:[ \t]+[A-Za-z]\.?)*[ \t]*(?:\r?\n|$)"
    return re.sub(pattern, "", text, flags=re.MULTILINE)
