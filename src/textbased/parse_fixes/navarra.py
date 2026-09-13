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
        text = text.replace(
            match.group(0),
            "Candidatura número: " + match.group(2) + ". " + match.group(1),
        )
    return text


@register_fixer("navarra", 1987, 6)
def fix_navarra_1987_06(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 1991, 5)
def fix_navarra_1991_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 1995, 5)
def fix_navarra_1995_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 1999, 6)
def fix_navarra_1999_06(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 2003, 5)
def fix_navarra_2003_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 2007, 5)
def fix_navarra_2007_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 2011, 5)
def fix_navarra_2011_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 2015, 5)
def fix_navarra_2015_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 2019, 5)
def fix_navarra_2019_05(text: str) -> str:
    text = _navarra_candidacy_fix(text)
    # Remove concejos
    if "proceso electoral en los concejos de Navarra" in text:
        text = text.split("proceso electoral en los concejos de Navarra")[0]
    return text


@register_fixer("navarra", 2023, 5)
def fix_navarra_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("5. Procedimiento Electoral", "")
    text = _navarra_candidacy_fix(text)
    return text
