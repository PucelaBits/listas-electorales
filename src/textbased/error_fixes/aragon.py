import re

from ._common import (
    autofill_missing_numbers,
    clean_ocr_numbers,
    fill_missing_numbers,
    register_fixer,
)


@register_fixer("aragon", 1991, 5)
def fix_aragon_1991_05(text: str) -> str:
    print(text)
    print(repr(text))
    text = text.replace("LISTA de candidaturas proclamadas por esta Jun-\n685\nta Electoral Provincial de Teruel", "Junta Electoral Provincial de Teruel")
    # Remove preamble
    text = text.replace(
        "\n1.cPARTIDO ARAGONES PAR.\n2.-PARTIDO SOCIALISTA DE LOS TRABA-\nJADORES PST.\n3.UNION ARAGONESISTA-CHUNTA-\nARAGONESISTA CHA.\n4.CENTRO DEMOCRATICO Y SOCIAL\nCDS.\n5.PARTIDO SOCIALISTA OBRERO ESPA-\nÑOL PSOE.\n6.CONVERGENCIA ALTERNATIVA DE\nARAGON-IZQUIERDA UNIDA. CAA-IU.\n7.PARTIDO POPULAR. PP.\n",
        "",
    )
    # Errata (err.pdf)
    text = text.replace(
        "3.UNION ARAGONESISTA-CHUNTA-\nARAGONESISTA CHA.",
        "3.CHUNTA ARAGONESISTA CHA",
    )
    text = text.replace(
        "3.UNION ARAGONESISTA-CHUNTA ARA-\nGONESISTA CHA",
        "3.CHUNTA ARAGONESISTA CHA",
    )
    # Fix OCR
    text = text.replace("N.2 5S", "5.")
    text = text.replace("N.25", "5.")
    text = clean_ocr_numbers(text)
    text = text.replace("14. Carlos Enrique Gabriel REYES RUBIO", "4. Carlos Enrique Gabriel REYES RUBIO")
    text = text.replace("4. PARTIDO SOCIALISTA DE LOS TRABAJA-\n", "4. PARTIDO SOCIALISTA DE LOS TRABAJA")
    text = text.replace("N.26 PÁARTIDO", "6. PARTIDO")
    text = text.replace("N 2.", "2.")
    text = text.replace("N.9. ", "9. ")
    text = text.replace("55.PARTIDO", "5. PARTIDO")
    text = text.replace("3.Miguel FORTEA CASTELLO", "13. Miguel FORTEA CASTELLO")
    text = text.replace("3. Agustín CLAVERO MARCO", "13. Agustín CLAVERO MARCO")
    text = text.replace("3. Miguel FORTEA CASTELLO", "13. Miguel FORTEA CASTELLO")
    text = text.replace("9 Francisco Javier DE JAIME LOREN", "9. Francisco Javier DE JAIME LOREN")
    text = text.replace("13 María del Carmen SAURA SICHAR", "13. María del Carmen SAURA SICHAR")
    text = text.replace("13 -María Pilar SERRANO EZQUERRA", "13. María Pilar SERRANO EZQUERRA")
    text = text.replace("26. Roberto Santiago MAYORA DOMECH", "25. Roberto Santiago MAYORA DOMECH")
    text = text.replace("Yo 12. Jovita BIEL FLETA-", "12. Jovita BIEL FLETA")
    text = text.replace("13. Custodio ARJONA CAÑADAS", "18. Custodio ARJONA CAÑADAS")
    text = autofill_missing_numbers(text)
    text = text.replace("GOMEZRODRIGUEZ", "GOMEZ RODRIGUEZ")
    text = text.replace("BASCONIDIMENEZ", "BASCON GIMENEZ")
    text = text.replace("AgustínAQUILUE", "Agustín AQUILUE")
    text = text.replace("ArturoGONZALVO", "Arturo GONZALVO")
    return text


def _fix_missing_substitutes(text: str, name_regex: re.Pattern) -> str:
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
        if line.upper() == "SUPLENTES":
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


_ARAGON_1995_05_NAME_REGEX = re.compile(
    r"^(?:DON|DOÑA)\s+[A-ZÁÉÍÓÚÜÑ]+(?:\s+[A-ZÁÉÍÓÚÜÑ]+)+$"
)


@register_fixer("aragon", 1995, 5)
def fix_aragon_1995_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("PEDRAFITA FERRER", "PIEDRAFITA FERRER")
    # Fix OCR
    text = text.replace(
        "S. FEDERACION DE LA PLATAFORMA", "5. FEDERACION DE LA PLATAFORMA"
    )
    text = text.replace("L PARTIDO ARAGONES", "1. PARTIDO ARAGONES")
    text = text.replace(
        "FEDERACION DE LA PLATAFORMA.\n", "FEDERACION DE LA PLATAFORMA "
    )
    text = text.replace("l ISIDORO ESTEBAN IZQUIERDO", "1. ISIDORO ESTEBAN IZQUIERDO")
    text = text.replace("E-MARÍA ANTONIA ROCA MUÑOZ", "14. MARÍA ANTONIA ROCA MUÑOZ")
    text = text.replace("'RICARDO SESE GINE", "15. RICARDO SESE GINE")
    text = text.replace("ROSA MARIA AGUILERA RUIZ", "4. ROSA MARIA AGUILERA RUIZ")
    text = text.replace("DOPEDDIAZ", "LÓPEZ DÍAZ")
    text = text.replace("1.SANTIAGO MONZON FLETA", "11. SANTIAGO MONZON FLETA")
    text = text.replace("DON FERNANDO LABENA GALLIZO", "4. DON FERNANDO LABENA GALLIZO")
    text = text.replace("DON CHESUS YUSTE CABELLO", "2. DON CHESUS YUSTE CABELLO")
    text = clean_ocr_numbers(text)
    text = autofill_missing_numbers(text)
    text = _fix_missing_substitutes(text, _ARAGON_1995_05_NAME_REGEX)
    return text


@register_fixer("aragon", 1999, 6)
def fix_aragon_1999_06(text: str) -> str:
    # Erratas (err.pdf)
    text = text.replace("MARTA DOLORES CANUDO AZOR", "MARÍA DOLORES CANUDO AZOR")
    # Make it easier to parse
    text = text.replace(
        "4.—S.O.S. NATURALEZA - LOS VERDES",
        "Candidatura núm.: 4. S.O.S. NATURALEZA - LOS VERDES",
    )
    return text


@register_fixer("aragon", 2003, 5)
def fix_aragon_2003_05(text: str) -> str:
    # Facilitate parsing
    text = text.replace("Nº ", "Candidatura núm.: ")
    if "2. VICTOR PEREZ ROCHE" in text:
        start_line = "2. VICTOR PEREZ ROCHE"
        end_line = "19. MARIA RUIZ GUERRERO"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    return text


def number_candidates(text: str, last_number: int | None = None) -> str:
    lines = text.split("\n")
    result = []
    counter = last_number

    for line in lines:
        stripped_line = line.lstrip()  # Remove leading whitespace for accurate checking

        # Check if the line is a candidate name
        if stripped_line.startswith(("DON ", "DOÑA ")) and counter is not None:
            # Add the number and increment the counter
            result.append(f"{counter}. {line}")
            counter += 1
            print(f"Numbering candidate: {line} as {counter - 1}")
        else:
            # Reset the counter if we hit a new list header or the "SUPLENTES" section
            upper_line = stripped_line.upper()
            if "CANDIDATURA NÚM." in upper_line or "SUPLENTES" in upper_line:
                counter = 1
                print(f"Resetting counter to 1 due to line: {line}")

            # Append the non-candidate line exactly as it was
            result.append(line)

    return "\n".join(result), counter


_ARAGON_2007_05_LAST_NUMBER = None


@register_fixer("aragon", 2007, 5)
def fix_aragon_2007_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "DOÑA MONSERRAT VILLAGRASA ALCANTARA",
        "DOÑA MONTSERRAT VILLAGRASA ALCANTARA",
    )
    text = text.replace("NIEVES IBERS VUELTA", "NIEVES IBEAS VUELTA")
    # Facilitate parsing
    text = text.replace("Nº ", "Candidatura núm.: ")
    text = text.replace("Nº", "Candidatura núm.: ")
    # Fill missing numbers
    global _ARAGON_2007_05_LAST_NUMBER
    print(_ARAGON_2007_05_LAST_NUMBER)
    text, last_number = number_candidates(text, last_number=_ARAGON_2007_05_LAST_NUMBER)
    _ARAGON_2007_05_LAST_NUMBER = last_number
    print(last_number)
    print(repr(text))
    return text


@register_fixer("aragon", 2011, 5)
def fix_aragon_2011_05(text: str) -> str:
    # Facilitate parsing
    text = text.replace("Nº ", "Candidatura núm.: ")
    return text
