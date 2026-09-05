import re
from collections.abc import Callable

ERROR_FIXERS: dict[tuple[str, int, int], Callable[[str], str]] = {}


def register_fixer(region: str, year: int, month: int):
    """Decorator to register a text-fixing function for a specific batch."""

    def decorator(func: Callable[[str], str]):
        ERROR_FIXERS[(region, year, month)] = func
        return func

    return decorator


def clean_ocr_text(text: str) -> str:
    """Cleans up common OCR errors in the text, such as stray punctuation, missing dots after numbers, and inconsistent formatting."""
    # Clean up "Núm" variations (e.g., "Núm.-", "Núm.- ", "Núm ")
    text = re.sub(r"Núm[\.\-\s]+", "Núm. ", text)

    # Remove stray quotes around numbers and dots
    text = re.sub(r"['´`\"](?=\d)", "", text)
    text = re.sub(r"(?<=\d)['´`\"]", "", text)
    text = re.sub(r"(?<=\d\.)['´`\"]", "", text)

    # Fix SINGLE colons and exclamation marks after numbers (e.g., "11:" -> "11.")
    text = re.sub(r"\b(\d+)[:!•]", r"\1.", text)

    # Fix CLUSTERS of messy punctuation (dots, dashes, commas, colons, exclamation marks)
    text = re.sub(r"\b(\d+)[\.\-\,:\!•]{2,}\s*", r"\1. ", text)

    # Fix stray dots before list numbers (e.g., ".13." -> "13.")
    text = re.sub(r"(?<=\s)[\.,](\d+)[\.,]", r"\1.", text)

    # Add missing dots after numbers preceding names/entities (e.g., "10 Don" -> "10. Don")
    text = re.sub(r"\b(\d+)\ +(?=Don|Doña|[A-Z]{2,})", r"\1. ", text)

    # Fix commas separating titles (e.g., "Don,Juan" -> "Don Juan")
    text = re.sub(r"(Don|Doña)[,|-]", r"\1 ", text)

    # Remove stray single letters surrounded by dots after numbers (e.g., "3.x. " -> "3. ")
    text = re.sub(r"\b(\d+)\.[a-zA-Z]\.\s*", r"\1. ", text)

    return text


_HAS_NUMBER_RE = re.compile(r"^\d+\.")


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
        if not _HAS_NUMBER_RE.match(line):
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
