import re

from common import NAME_WHITELIST_CHARS

from ._common import (
    UPPER_CANDIDATE_REGEX,
    number_candidates,
    register_fixer,
)

_NAVARRA_CANDIDACY_REGEX = re.compile(
    rf"^([{NAME_WHITELIST_CHARS} \d\+/]+(?:\s+\(.+\))?)\s+\(R\-(\d+)\)$",
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
    # Fix wrong numbering
    text = text.replace("(R-21)", "(R-1)")
    text = text.replace("(R-67)", "(R-2)")
    text = text.replace("(R-109)", "(R-3)")
    text = text.replace("(R-242)", "(R-4)")
    text = text.replace("(R-511)", "(R-5)")
    text = text.replace("(R-606)", "(R-6)")
    text = text.replace("(R-603)", "(R-7)")
    text = text.replace("(R-736)", "(R-8)")
    text = text.replace("(R-785)", "(R-9)")
    text = _navarra_candidacy_fix(text)
    return text


@register_fixer("navarra", 2011, 5)
def fix_navarra_2011_05(text: str) -> str:
    # Remove concejos
    if "JUNTA ELECTORAL DE ZONA DE AOIZ" in text:
        text = text.split("JUNTA ELECTORAL DE ZONA DE AOIZ")[0]
    text = _navarra_candidacy_fix(text)
    return text


_NAVARRA_2015_05_LAST_NUMBER = None


@register_fixer("navarra", 2015, 5)
def fix_navarra_2015_05(text: str) -> str:
    # Remove preamble
    text = text.replace("ANEXO\n", "")
    # Remove concejos
    if "JUNTA ELECTORAL DE ZONA DE AOIZ" in text:
        text = text.split("JUNTA ELECTORAL DE ZONA DE AOIZ")[0]
    text = text.replace("PODEMOS (R-5)", "PODEMOS (R-8)")
    text = text.replace("(9-11", "(R-11)")
    text = _navarra_candidacy_fix(text)
    # Fix OCR errors
    text = text.replace("lOS", "IOS")
    text = text.replace(":OIO", "GOIO")
    text = text.replace("PORRA:", "PORRAS")
    text = text.replace("IÑAKI)", "IÑAKI")
    text = text.replace("'OLESEA DONTU Di", "OLESEA DONTU DONTU")
    text = text.replace("BS DE\n", "")
    text = text.replace("FS RRA", "")
    text = text.replace("4u RAFAEL", "RAFAEL")
    text = text.replace("u BIKENDI BAREA AIESTARAN", "11. BIKENDI BAREA AIESTARAN")
    text = text.replace(
        "JOSE MIGUEL BERNAL HIERRO\n", "JOSE MIGUEL BERNAL HIERRO DE ONA"
    )
    text = text.replace("PATRICIA DE PEDRO APARI:", "PATRICIA DE PEDRO APARICIO")
    text = text.replace("2015\nDE ONA\n", "2015\n")
    text = text.replace("1OSU", "IOSU")
    global _NAVARRA_2015_05_LAST_NUMBER
    text, last_number = number_candidates(
        text, UPPER_CANDIDATE_REGEX, _NAVARRA_2015_05_LAST_NUMBER
    )
    _NAVARRA_2015_05_LAST_NUMBER = last_number
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
