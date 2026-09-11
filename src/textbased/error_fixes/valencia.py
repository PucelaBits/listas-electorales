import re

from ._common import register_fixer


def _valencia_dedouble_fix(text: str) -> str:
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


@register_fixer("valencia", 2023, 5)
def fix_valencia_2023_05(text: str) -> str:
    text = _valencia_dedouble_fix(text)
    if "MARÍA AMPARO GINER LOZANO" in text:
        # Replace all XX, with XX.
        text = re.sub(r"(\d+),", r"\1.", text)
    return text
