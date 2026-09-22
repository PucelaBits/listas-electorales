import re

from ._common import LOWER_CANDIDATE_REGEX, fix_missing_substitute_numbers, register_fixer

_BOIB_REGEX = re.compile(r"^.*BOIB.*$", re.MULTILINE)


def _baleares_province_fix(text: str) -> str:
    suffix = 1
    if "consejos insulares" in text.lower():
        suffix = 10
    text = text.replace("Mallorca\n", f"BALE-{suffix}\n")
    text = text.replace("MALLORCA\n", f"BALE-{suffix}\n")
    text = text.replace("Ibiza\n", f"BALE-{suffix + 1}\n")
    text = text.replace("IBIZA\n", f"BALE-{suffix + 1}\n")
    text = text.replace("Eivissa\n", f"BALE-{suffix + 1}\n")
    text = text.replace("EIVISSA\n", f"BALE-{suffix + 1}\n")
    text = text.replace("Menorca\n", f"BALE-{suffix + 2}\n")
    text = text.replace("MENORCA\n", f"BALE-{suffix + 2}\n")
    text = text.replace("Formentera\n", f"BALE-{suffix + 3}\n")
    text = text.replace("FORMENTERA\n", f"BALE-{suffix + 3}\n")
    text = text.replace("Sant Antoni de Portmany\n", f"BALE-{suffix + 4}\n")
    text = text.replace("Sant Josep de sa Talaia\n", f"BALE-{suffix + 5}\n")
    text = text.replace("Sant Joan de Labritja\n", f"BALE-{suffix + 6}\n")
    text = text.replace("Santa Eulària des Riu\n", f"BALE-{suffix + 7}\n")
    return text


_BALEARES_CANDIDACY_REPRESENTATION_REGEX = re.compile(
    r"En representac[ií][óo]n(?: de)?: *(.+\n?.+)$", re.MULTILINE | re.IGNORECASE
)


def _baleares_candidacy_representation_fix(
    text: str, last_index: int
) -> tuple[str, int]:
    current_index = last_index
    for line in text.splitlines():
        line_lower = line.lower()
        if "circunscripción" in line_lower or "circumscripció" in line_lower:
            current_index = 1
            continue
        match = _BALEARES_CANDIDACY_REPRESENTATION_REGEX.match(line)
        if match:
            candidacy = match.group(1).strip()
            text = text.replace(line, f"Candidatura núm. {current_index}: {candidacy}")
            current_index += 1
        elif "en representació " in line_lower:
            # This is repeated for each candidacy, so we can just remove it
            text = text.replace(line, "")
    return text, current_index


@register_fixer("baleares", 1983, 5)
def fix_baleares_1983_05(text: str) -> str:
    # Remove header
    if "JUNTA ELECTORAL DE BALEARES" in text:
        text = text.split("JUNTA ELECTORAL DE BALEARES")[-1]
    # Remove footer
    if "JUNTA ELECTORAL DE MADRID" in text:
        text = text.split("JUNTA ELECTORAL DE MADRID")[0]
    text = _baleares_province_fix(text)
    return text


_BALEARES_1987_06_CANDIDACY_INDEX = 1


@register_fixer("baleares", 1987, 6)
def fix_baleares_1987_06(text: str) -> str:
    text = _baleares_province_fix(text)
    global _BALEARES_1987_06_CANDIDACY_INDEX
    text, _BALEARES_1987_06_CANDIDACY_INDEX = _baleares_candidacy_representation_fix(
        text, _BALEARES_1987_06_CANDIDACY_INDEX
    )
    return text


_BALEARES_1991_05_CANDIDACY_INDEX = 1


@register_fixer("baleares", 1991, 5)
def fix_baleares_1991_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("Luis Marín Pallas", "Antonio Durán Cañellas")
    text = text.replace("Llofri u", "Llufriu")
    text = text.replace("Catalina Serar Tur", "Catalina Serra Tur")
    text = text.replace("José Pedraza Pérez\nsuplentes", "José Pedraza Pérez")
    text = text.replace("Marinao Uobet Roman", "Mariano Llobet Roman")
    text = text.replace("Isael Ferrer Arabi", "Isabel Ferrer Arabi")
    text = _baleares_province_fix(text)
    global _BALEARES_1991_05_CANDIDACY_INDEX
    text, _BALEARES_1991_05_CANDIDACY_INDEX = _baleares_candidacy_representation_fix(
        text, _BALEARES_1991_05_CANDIDACY_INDEX
    )
    return text


_BALEARES_1995_05_CANDIDACY_INDEX = 1


@register_fixer("baleares", 1995, 5)
def fix_baleares_1995_05(text: str) -> str:
    text = _baleares_province_fix(text)
    global _BALEARES_1995_05_CANDIDACY_INDEX
    text, _BALEARES_1995_05_CANDIDACY_INDEX = _baleares_candidacy_representation_fix(
        text, _BALEARES_1995_05_CANDIDACY_INDEX
    )
    return text


@register_fixer("baleares", 1999, 6)
def fix_baleares_1999_06(text: str) -> str:
    text = _baleares_province_fix(text)
    # TODO: Missing candidacies numbers
    return text


_BALEARES_2003_05_CANDIDACY_INDEX = 1


@register_fixer("baleares", 2003, 5)
def fix_baleares_2003_05(text: str) -> str:
    text = _baleares_province_fix(text)
    global _BALEARES_2003_05_CANDIDACY_INDEX
    text, _BALEARES_2003_05_CANDIDACY_INDEX = _baleares_candidacy_representation_fix(
        text, _BALEARES_2003_05_CANDIDACY_INDEX
    )
    # Remove lines that contain BOIB
    text = _BOIB_REGEX.sub("", text)
    # Fix substitutes
    text = text.replace(
        "14 Angel Marqués Saurina", "Suplentes\n14 Angel Marqués Saurina"
    )
    text = text.replace("14 Miquel Pons Victori", "Suplentes\n14 Miquel Pons Victori")
    text = text.replace("5 Eduvigis Sánchez Meroño", "3 Eduvigis Sánchez Meroño")
    text = fix_missing_substitute_numbers(text, LOWER_CANDIDATE_REGEX)
    return text


_BALEARES_2007_05_FIRST_1_SUBSTITUTE_REGEX = re.compile(
    r"^1 (.+) Suplente$", re.MULTILINE
)
_BALEARES_2007_05_FIRST_34_SUBSTITUTE_REGEX = re.compile(
    r"^34 (.+) Suplente$", re.MULTILINE
)
_BALEARES_2007_05_REPEAT_FIRST_SUBSTITUTE_REGEX = re.compile(
    r"^Suplente nº 1(.+)$", re.MULTILINE
)


@register_fixer("baleares", 2007, 5)
def fix_baleares_2007_05(text: str) -> str:
    # Remove preamble
    if "Consorcio, para cumplir sus finalidades, puede realiz" in text:
        return ""
    if "Consorci, per acomplir les seves finalitats" in text:
        text = text.split("Consorci, per acomplir les seves finalitats")[-1]
    text = text.replace(
        "UNIÓ CENTRISTES DE MENORCA\n", "UNIÓ CENTRISTES DE MENORCA (UCM)\n"
    )
    text = _baleares_province_fix(text)
    text = text.replace("Nº Candidato/a Formación Política", "")
    text = text.replace("Nº Candidato/a\nFormación Política", "")
    text = text.replace("Num ", "Candidatura núm. ")
    text = text.replace("Num7", "Candidatura núm. 7")
    # Remove lines that contain BOIB
    text = _BOIB_REGEX.sub("", text)
    # Replace the first substitute line
    text = _BALEARES_2007_05_FIRST_1_SUBSTITUTE_REGEX.sub(r"Suplentes\n1 \1", text)
    text = _BALEARES_2007_05_FIRST_34_SUBSTITUTE_REGEX.sub(r"Suplentes\n34 \1", text)
    text = _BALEARES_2007_05_REPEAT_FIRST_SUBSTITUTE_REGEX.sub(r"Suplentes\n1 \1", text)
    text = text.replace(" Suplente", "")
    text = text.replace("Suplente nº ", "")
    text = text.replace(
        "34 Sra. Laura Maria Bryant Forteza Independiente",
        "SUPLENTES\n34 Sra. Laura Maria Bryant Forteza",
    )
    text = text.replace(
        "34 Sr. Mateo Morro Latorre", "SUPLENTES\n34 Sr. Mateo Morro Latorre"
    )
    text = text.replace("PARTIDO SOCIALISTA OBRERO\n", "PARTIDO SOCIALISTA OBRERO ")
    text = text.replace(
        "2\n3 DON JAVIER ABRIL DE COO\nDOÑA MARIA JESUS MATA RODILANA",
        "2 DON JAVIER ABRIL DE COO\n3 DOÑA MARIA JESUS MATA RODILANA",
    )
    # Missing candidacies
    text = text.replace("\nPARTIDO POPULAR", "\nCandidatura núm. 1 PARTIDO POPULAR")
    text = text.replace(
        "\nPARTIDO SOCIALISTA OBRERO ESPAÑOL",
        "\nCandidatura núm. 2 PARTIDO SOCIALISTA OBRERO ESPAÑOL",
    )
    text = text.replace(
        "\nESQUERRA DE MENORCA-ESQUERRA UNIDA",
        "\nCandidatura núm. 3 ESQUERRA DE MENORCA-ESQUERRA UNIDA",
    )
    text = text.replace(
        "\nCOALICIÓ ELECTORAL PARTIT SOCIALISTA DE MENORCA-ENTESA",
        "\nCandidatura núm. 4 COALICIÓ ELECTORAL PARTIT SOCIALISTA DE MENORCA-ENTESA",
    )
    text = text.replace(
        "\nUNIÓ CENTRISTES DE MENORCA",
        "\nCandidatura núm. 5 UNIÓ CENTRISTES DE MENORCA",
    )
    text = text.replace(
        "\nCIUDADANOS EN BLANCO", "\nCandidatura núm. 6 CIUDADANOS EN BLANCO"
    )
    return text


@register_fixer("baleares", 2011, 5)
def fix_baleares_2011_05(text: str) -> str:
    text = _baleares_province_fix(text)
    # Errata (err.pdf)
    text = text.replace(
        "1.\nSra. ELISA CRESPI ORELL\n2.\nSr. FRANCISCO FERNANDEZ OCHOA",
        "1.\nSr. FRANCISCO FERNANDEZ OCHOA\n2.\nSra. ELISA CRESPI ORELL",
    )
    # Remove lines that contain BOIB
    text = _BOIB_REGEX.sub("", text)
    text = text.replace("Orden Nombre y apellidos", "")
    return text


@register_fixer("baleares", 2015, 5)
def fix_baleares_2015_05(text: str) -> str:
    text = _baleares_province_fix(text)
    return text


@register_fixer("baleares", 2019, 5)
def fix_baleares_2019_05(text: str) -> str:
    # Remove zero-width space characters (U+200B)
    text = text.replace("\u200b", "")
    text = text.replace(
        "Fascículo 89 - Sec. V. - Pág. 17702",
        "Fascículo 89 - Sec. V. - Pág. 17702\nElecciones a los Consejos Insulares de 2019",
    )
    text = text.replace(
        "Fascículo 89 - Sec. V. - Pág. 17737",
        "Fascículo 89 - Sec. V. - Pág. 17737\nElecciones a los Consejos Insulares de 2019",
    )
    text = _baleares_province_fix(text)
    # Fix error
    text = text.replace(
        "4. JUAN FRANCISCO TORRES SERRA", "3. JUAN FRANCISCO TORRES SERRA"
    )
    return text


@register_fixer("baleares", 2023, 5)
def fix_baleares_2023_05(text: str) -> str:
    text = _baleares_province_fix(text)
    return text
