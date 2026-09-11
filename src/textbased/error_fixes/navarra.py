import re

from common import NAME_WHITELIST_CHARS

from ._common import register_fixer

_NAVARRA_CANDIDACY_REGEX = re.compile(
    r"^([" + NAME_WHITELIST_CHARS + r"\s\(\)\+/]+) +\(R\-(\d+)\)$",
    re.MULTILINE,
)


def _navarra_candidacy_fix(text: str) -> str:
    for match in re.finditer(_NAVARRA_CANDIDACY_REGEX, text):
        # We want to write "Candidatura número: X" followed by the name
        text = text.replace(match.group(0), "Candidatura número: " + match.group(2) + ". " + match.group(1))
    return text


@register_fixer("navarra", 2023, 5)
def fix_navarra_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("5. Procedimiento Electoral", "")
    text = _navarra_candidacy_fix(text)
    return text
