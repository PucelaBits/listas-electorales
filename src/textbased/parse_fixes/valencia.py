import re

from ._common import register_fixer


def _fix_valencia_dedouble(text: str) -> str:
    """
    Some of Valencia BO documents are half in Valencian and half in Spanish.
    We remove the Valencian part, which is always first, and keep the Spanish part, which is always second.
    We keep the Spanish part to facilitate the parsing.
    """
    # Look for the last line of the text and search when it appears again
    # If it appears more than twice, we raise an error, because we don't know which one to keep
    last_line = text.splitlines()[-1]
    last_line_count = text.count(last_line)
    if last_line_count > 2:
        raise ValueError(
            f"Last line '{last_line}' appears {last_line_count} times in the text. Cannot dedouble."
        )
    # If it appears only once, we keep the text from the last line onwards
    last_line_index = text.find(last_line)
    text = text[last_line_index + len(last_line) :]
    return text


_VALENCIA_PROVINCE_REGEX = re.compile(
    r"(?i)\b(?:alacant\s*/\s*alicante|alicante\s*/\s*alacant|"
    r"castell[óo]\s*/\s*castell[óo]n|castell[óo]n\s*/\s*castell[óo]|"
    r"val[èe]ncia\s*/\s*valencia|valencia\s*/\s*val[èe]ncia)\b"
)


def _fix_valencia_province(text: str) -> str:
    def replacement(match):
        matched_str = match.group(0).upper()

        # Check which province was matched and return the corresponding string
        if "ALICANTE" in matched_str:
            return "Circunscripción electoral: ALICANTE"
        if "CASTELL" in matched_str:
            return "Circunscripción electoral: CASTELLÓN"
        if "VALEN" in matched_str:
            return "Circunscripción electoral: VALENCIA"

        return match.group(0)

    return re.sub(_VALENCIA_PROVINCE_REGEX, replacement, text)


def _fix_valencia_substitutes(text: str) -> str:
    text = text.replace("\nS1", "\nSUPLENTES\n1.")
    text = text.replace("\nS2", "\nSUPLENTES\n2.")
    text = text.replace("\nS3", "\nSUPLENTES\n3.")
    text = text.replace("\nS4", "\nSUPLENTES\n4.")
    text = text.replace("\nS5", "\nSUPLENTES\n5.")
    text = text.replace("\nS6", "\nSUPLENTES\n6.")
    text = text.replace("\nS7", "\nSUPLENTES\n7.")
    text = text.replace("\nS8", "\nSUPLENTES\n8.")
    text = text.replace("\nS9", "\nSUPLENTES\n9.")
    text = text.replace("\nS10", "\nSUPLENTES\n10.")
    return text


@register_fixer("valencia", 1983, 5)
def fix_valencia_1983_05(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1987, 6)
def fix_valencia_1987_06(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1991, 5)
def fix_valencia_1991_05(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1995, 5)
def fix_valencia_1995_05(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1999, 6)
def fix_valencia_1999_06(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 2003, 5)
def fix_valencia_2003_05(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_substitutes(text)
    return text


@register_fixer("valencia", 2007, 5)
def fix_valencia_2007_05(text: str) -> str:
    # Remove preamble
    if "Anuncio del Ministerio de Fomento" in text:
        return ""
    text = _fix_valencia_province(text)
    text = _fix_valencia_substitutes(text)
    text = text.replace("CADIDATURA", "CANDIDATURA")
    text = text.replace("N.º orden presentación", "Candidatura núm.")
    # TODO: Remove location at the end of the names
    return text


@register_fixer("valencia", 2011, 5)
def fix_valencia_2011_05(text: str) -> str:
    # TODO: err.pdf
    text = _fix_valencia_province(text)
    text = text.replace("Núm. Ord. Pres.", "Candidatura núm.")
    text = text.replace("Nº Ord. Pres:", "Candidatura núm.")
    text = _fix_valencia_substitutes(text)
    return text


@register_fixer("valencia", 2015, 5)
def fix_valencia_2015_05(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_dedouble(text)
    return text


@register_fixer("valencia", 2019, 4)
def fix_valencia_2019_04(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_dedouble(text)
    return text


@register_fixer("valencia", 2023, 5)
def fix_valencia_2023_05(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_dedouble(text)
    if "MARÍA AMPARO GINER LOZANO" in text:
        # Replace all XX, with XX.
        text = re.sub(r"(\d+),", r"\1.", text)
    return text
