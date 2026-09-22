import re
from collections.abc import Callable

from common import (
    NAME_WHITELIST_CHARS,
    NAME_WHITELIST_CHARS_LOWER,
    NAME_WHITELIST_CHARS_UPPER,
)

NUMBER_MAP = {
    "UNO": "1",
    "DOS": "2",
    "TRES": "3",
    "CUATRO": "4",
    "CINCO": "5",
    "SEIS": "6",
    "SIETE": "7",
    "OCHO": "8",
    "NUEVE": "9",
    "DIEZ": "10",
}

PARSE_FIXES: dict[tuple[str, int, int], Callable[[str], str]] = {}

UPPER_CANDIDATE_REGEX = re.compile(
    rf"^(?!NO PROCLAMADA)(?:[{NAME_WHITELIST_CHARS_UPPER}\.]+ +(?:DE +|LOS +|DEL +|LA +)*){{1,2}}(?:\([{NAME_WHITELIST_CHARS_UPPER}\. ]+\) +(?:DE +|LOS +|DEL +|LA +)*)?(?:[{NAME_WHITELIST_CHARS_UPPER}\.]+ *(?:DE +|LOS +|DEL +|LA +)*){{1,4}}(?:\([{NAME_WHITELIST_CHARS}\. ]+\))? *\.?$"
)
LOWER_CANDIDATE_REGEX = re.compile(
    rf"^(?!NO PROCLAMADA)(?:[{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER}]+ +(?:de +|los +|del +|la +)*){{1,2}}(?:\([{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER} ]+\) +(?:de +|los +|del +|la +)*)?(?:[{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER}]+ *(?:de +|los +|del +|la +)*){{1,3}}(?:\([{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER} ]+\))? *\.?$"
)
UPPER_DON_CANDIDATE_NAME_REGEX = re.compile(
    rf"^(?:DON|DOÑA|Don|Doña|D.|Dª)\s+(?:[{NAME_WHITELIST_CHARS_UPPER}]+|FCO\.)(?:\s+[{NAME_WHITELIST_CHARS_UPPER}]+|\s+[{NAME_WHITELIST_CHARS_UPPER}]\.|\s+FCO\.|\s+\(.+\))+\.?$"
)
LOWER_DON_CANDIDATE_NAME_REGEX = re.compile(
    rf"^(?:Don|Doña|D.|Dª)\s+[{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER}]+(?:(?:\s+|\s?\-\s?)[{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER}]+|\s+y|\s+del|\s+las?|\s+de|\s+los|\s+[{NAME_WHITELIST_CHARS_UPPER}]\.)+\.?$"
)

_MULTILINE_CANDIDACY_RE = re.compile(
    r"(\d+)\s+(?:FORMACIÓN POLÍTICA:|DENOMINACIÓN:?)\s+(.+)\s+SIGLAS:?\s*(.+)$",
    re.MULTILINE | re.IGNORECASE,
)
_MULTILINE_INVERSE_CANDIDACY_RE = re.compile(
    r"^SIGLAS:\s*(.*)[\n\r]PART/FED(?:ER)?/AGRUP:\s*(.+\s*.+)[\n\r]CANDIDATURA Nº:?\s*(\d+)\.?$",
    re.MULTILINE | re.IGNORECASE,
)
_MULTILINE_NOT_PROCLAIMED_CANDIDACY_RE = re.compile(
    r"N[UÚ]M\.(?:DE +ORDEN)?\s*(\d+)\s+NO PROCLAMADA$", re.MULTILINE | re.IGNORECASE
)


def fix_maria_ocr(text: str, upper: bool = False) -> str:
    replace_text = "María" if not upper else "MARÍA"
    text = text.replace("M1. ", f"{replace_text} ")
    text = text.replace("M1 ", f"{replace_text} ")
    text = text.replace("M2. ", f"{replace_text} ")
    text = text.replace("M2 ", f"{replace_text} ")
    text = text.replace("Mª.", f"{replace_text}")
    text = text.replace("M.ª", f"{replace_text}")
    text = text.replace("M.2", f"{replace_text}")
    text = text.replace(" M . ", f" {replace_text} ")
    text = text.replace(" M ", f" {replace_text} ")
    text = text.replace(" M. ", f" {replace_text} ")
    text = text.replace(" MI ", f" {replace_text} ")
    return text


def fix_multiline_candidacy_naming(text: str) -> str:
    text = _MULTILINE_CANDIDACY_RE.sub(r"\1: \2 (\3)", text)
    text = _MULTILINE_INVERSE_CANDIDACY_RE.sub(r"Candidatura núm. \3: \2 (\1)", text)
    text = _MULTILINE_NOT_PROCLAIMED_CANDIDACY_RE.sub(
        r"Candidatura núm. \1: RELLENO\nNO PROCLAMADA", text
    )
    return text


def register_fixer(region: str, year: int, month: int):
    """Decorator to register a text-fixing function for a specific batch."""

    def decorator(func: Callable[[str], str]):
        PARSE_FIXES[(region, year, month)] = func
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
    text = re.sub(r"^l[\.|:]", "1.", text, flags=re.MULTILINE)
    text = re.sub(r"^S\.", "5.", text, flags=re.MULTILINE)
    # Fixes candidacies Nº
    text = re.sub(
        r"Candidatura\.? +[\w'\.]{1,4} (\d+)+ *\.?",
        r"Candidatura número: \1.",
        text,
        flags=re.MULTILINE | re.IGNORECASE,
    )
    # Replaces the stuff before a number with the number
    text = re.sub(r"^[\w\.']{1,3} +(\d+)\.?", r"\1.", text, flags=re.MULTILINE)
    # Remove stray quotes around numbers and dots
    text = re.sub(r"['´`\"](?=\d)", "", text)
    text = re.sub(r"(?<=\d)['´`\"]", "", text)
    text = re.sub(r"(?<=\d\.)['´`\"]", "", text)

    # Fix CLUSTERS of messy punctuation (dots, dashes, commas, colons, exclamation marks)
    text = re.sub(r"\b(\d+)\s*[\.\-\,:\!•'·;\"]{2,}\s*", r"\1. ", text)

    # Fix stray dots before list numbers (e.g., ".13." -> "13.")
    text = re.sub(
        re.compile(
            r"^(?:[']*Núm\.?)?\ *[\.\-\,:\!•'·;\"]\ *(\d+)\ *[\.]\ *[\.\-\,:\!•'·;\"]*",
            re.MULTILINE,
        ),
        r"\1. ",
        text,
    )
    # Remove stray single letters surrounded by dots after numbers (e.g., "3.x. " -> "3. ")
    text = re.sub(r"\b(\d+)\.[a-zA-Z]\.\s*", r"\1. ", text)

    return text


_HAS_NUMBER_RE = re.compile(r"^(\d+)\.?")


def autofill_intermediate_numbers(text: str) -> str:
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


def remove_single_letter_lines(text: str) -> str:
    """
    Removes lines that consist of a single letter (A-Z, a-z) or multiple single
    letters separated by spaces, optionally followed by dots.
    """
    pattern = r"^[ \t]*[A-Za-z]\.?(?:[ \t]+[A-Za-z]\.?)*[ \t]*(?:\r?\n|$)"
    return re.sub(pattern, "", text, flags=re.MULTILINE)


def fix_missing_substitutes(text: str, name_regex: re.Pattern) -> str:
    """
    Fixes missing substitutes in the text.
    This function looks for specific patterns in the text where substitutes numbers are missing
    """
    lines = text.splitlines()
    fixed_lines = []
    candidate_order = None
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.upper().startswith("SUPLENTE"):
            # Check if the next line is a number; if not, insert the missing number
            candidate_order = 1
        elif candidate_order is not None:
            if line.startswith(f"{candidate_order}."):
                # Correctly numbered line, move to the next candidate
                candidate_order += 1
            elif line[0].isdigit():
                # Other numbered line, but not the expected one; reset candidate_order
                candidate_order = None
            elif name_regex.match(line):
                # Missing number, insert it
                fixed_lines.append(f"{candidate_order}. {line}")
                candidate_order += 1
                continue
        fixed_lines.append(line)
    return "\n".join(fixed_lines)


def number_candidates(
    text: str, candidate_regex: re.Pattern, last_number: int | None = None
) -> str:
    """
    Automatically numbers candidates in the text, starting from last_number if provided.
    It overrides numbers in the text if present
    """
    lines = text.split("\n")
    result = []
    counter = last_number

    for line in lines:
        stripped_line = line.lstrip()  # Remove leading whitespace for accurate checking
        upper_line = stripped_line.upper()

        # Reset the counter if we hit a new list header or the "SUPLENTES" section
        if (
            "CANDIDATURA NÚM" in upper_line
            or "SUPLENTES" in upper_line
            or "ELECTORAL" in upper_line
            or "SECRETARIO " in upper_line
        ):
            counter = 1
            result.append(line)
            continue
        # Check if the line is a candidate name
        number_match = _HAS_NUMBER_RE.match(stripped_line)
        if number_match and counter is not None:
            # Override the number with the current counter if the line is a candidate name
            candidate_name = stripped_line[number_match.end() :].lstrip()
            if candidate_regex.match(candidate_name):
                result.append(
                    f"{counter}. {stripped_line[number_match.end() :].lstrip()}"
                )
                counter += 1
            else:
                result.append(line)  # Not a candidate name, keep the line as is
            continue
        if candidate_regex.match(stripped_line) and counter is not None:
            # Add the number and increment the counter
            result.append(f"{counter}. {line}")
            counter += 1
            continue

        # Append the non-candidate line exactly as it was
        result.append(line)

    return "\n".join(result), counter
