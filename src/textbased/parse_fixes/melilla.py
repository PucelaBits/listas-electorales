import re

from ._common import NUMBER_MAP, number_candidates, register_fixer

_MELILLA_2015_05_LAST_NUMBER = None
_MELILLA_2015_05_CANDIDATE_REGEX = re.compile(r"^(?:Don|Doña) (.+)$")


@register_fixer("melilla", 2007, 5)
def fix_melilla_2007_05(text: str) -> str:
    # Remove preamble
    text = text.replace("16.- D. FERNANDO CAVA GARCÍA, Secretario de la Junta Electoral.", "")
    # Facilitate parse
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text} ", f"CANDIDATURA NÚM. {number} "
        )
    return text


@register_fixer("melilla", 2011, 5)
def fix_melilla_2011_05(text: str) -> str:
    # Remove preamble
    if "dos de abril (Boletín Oficial del Estado. núm. 80, martes tre" in text:
        return "Circunscripción electoral de Melilla"
    return text


@register_fixer("melilla", 2015, 5)
def fix_melilla_2015_05(text: str) -> str:
    # Remove preamble
    if "236. CIUDAD AUTÓNOMA" in text:
        return ""
    text = text.replace(
        "Doña María Fernanda Álvarez De Los Corrales Melgar\n23",
        "23. Doña María Fernanda Álvarez De Los Corrales Melgar",
    )
    global _MELILLA_2015_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        _MELILLA_2015_05_CANDIDATE_REGEX,
        last_number=_MELILLA_2015_05_LAST_NUMBER,
    )
    _MELILLA_2015_05_LAST_NUMBER = last_number
    return text


@register_fixer("melilla", 2019, 5)
def fix_melilla_2019_05(text: str) -> str:
    # TODO: err.pdf
    text = text.replace(
        "26. Suplentes\n27. Rosa María Montero Madrid\n28. Oliverio Sánchez Vargas\n29. María Consuelo Guerra Muñoz",
        "Suplentes\n1. Rosa María Montero Madrid\n2. Oliverio Sánchez Vargas\n3. María Consuelo Guerra Muñoz",
    )
    text = text.replace(
        "Candidatura núm. 8: COALICION POR MELILLA (CPM)\nNo proclamada\nCandidatura núm. 9: AHORA MELILLA (AHORA MELILLA)\nNo proclamada\n",
        "",
    )
    return text


@register_fixer("melilla", 2023, 5)
def fix_melilla_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("120. PROCLAMACIÓN CANDIDATURAS", "")
    return text
