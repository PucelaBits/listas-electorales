from ._common import (
    UPPER_DON_CANDIDATE_NAME_REGEX,
    autofill_intermediate_numbers,
    clean_ocr_numbers,
    fill_missing_numbers,
    fix_missing_substitute_numbers,
    number_candidates,
    register_fixer,
)


@register_fixer("aragon", 1983, 5)
def fix_aragon_1983_05(text: str) -> str:
    # Fix OCR
    text = text.replace("Cortes de Aragón de 1983:", "")
    text = text.replace("Mariano.Ruperto.José", "Mariano-Ruperto-José")
    text = text.replace("D.a\nGloria", "D.a Gloria")
    text = text.replace("Nada!", "Nadal")
    text = clean_ocr_numbers(text)
    # Manually fix missing "SUPLENTES"
    if "Sixto Luis Agudo" in text or "Javier Escartín Orús" in text:
        text = text.replace("19.", "\nSUPLENTES\n19.")
    text = fix_missing_substitute_numbers(text, UPPER_DON_CANDIDATE_NAME_REGEX)
    return text


@register_fixer("aragon", 1987, 6)
def fix_aragon_1987_06(text: str) -> str:
    # Fix OCR
    text = text.replace("N2 L", "1.")
    text = text.replace("N2 L", "1.")
    text = text.replace("N7 5.", "5.")
    text = text.replace("I.Cesáreo", "1. Cesáreo")
    text = text.replace("JuliaCAMBRA", "Julia CAMBRA")
    text = text.replace("Marcos'NARRO", "Marcos NARRO")
    text = text.replace("Lucio HERNANDEZ\n", "Lucio HERNANDEZ ")
    text = clean_ocr_numbers(text)
    return text


@register_fixer("aragon", 1991, 5)
def fix_aragon_1991_05(text: str) -> str:
    text = text.replace(
        "LISTA de candidaturas proclamadas por esta Jun-\n685\nta Electoral Provincial de Teruel",
        "Junta Electoral Provincial de Teruel",
    )
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
    text = text.replace(
        "14. Carlos Enrique Gabriel REYES RUBIO",
        "4. Carlos Enrique Gabriel REYES RUBIO",
    )
    text = text.replace(
        "4. PARTIDO SOCIALISTA DE LOS TRABAJA-\n",
        "4. PARTIDO SOCIALISTA DE LOS TRABAJA",
    )
    text = text.replace("N.26. PÁARTIDO", "6. PARTIDO")
    text = text.replace("N.9. ", "9. ")
    text = text.replace("55.PARTIDO", "5. PARTIDO")
    text = text.replace("3.Miguel FORTEA CASTELLO", "13. Miguel FORTEA CASTELLO")
    text = text.replace("3. Agustín CLAVERO MARCO", "13. Agustín CLAVERO MARCO")
    text = text.replace(
        "13 -María Pilar SERRANO EZQUERRA", "13. María Pilar SERRANO EZQUERRA"
    )
    text = text.replace(
        "26.Roberto Santiago MAYORA DOMECH", "25. Roberto Santiago MAYORA DOMECH"
    )
    text = text.replace("Yo 12. Jovita BIEL FLETA-", "12. Jovita BIEL FLETA")
    text = text.replace("13.Custodio ARJONA CAÑADAS", "18. Custodio ARJONA CAÑADAS")
    text = autofill_intermediate_numbers(text)
    text = text.replace("GOMEZRODRIGUEZ", "GOMEZ RODRIGUEZ")
    text = text.replace("BASCONIDIMENEZ", "BASCON GIMENEZ")
    text = text.replace("AgustínAQUILUE", "Agustín AQUILUE")
    text = text.replace("ArturoGONZALVO", "Arturo GONZALVO")
    text = text.replace("ía AYALA BELTRAN", "María AYALA BELTRAN")
    return text


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
    text = text.replace("MARCOS.RUBIO SAHUN", "MARCOS RUBIO SAHUN")
    text = clean_ocr_numbers(text)
    text = autofill_intermediate_numbers(text)
    text = fix_missing_substitute_numbers(text, UPPER_DON_CANDIDATE_NAME_REGEX)
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
    text = text.replace(
        "4. PARTIDO SOCIALISTA OBRERO ESPAÑOL\n",
        "4. PARTIDO SOCIALISTA OBRERO ESPAÑOL ",
    )
    # Fill missing numbers
    global _ARAGON_2007_05_LAST_NUMBER
    if "Electoral Provincial de Huesca" in text:
        text, last_number = number_candidates(
            text, UPPER_DON_CANDIDATE_NAME_REGEX, last_number=_ARAGON_2007_05_LAST_NUMBER
        )
        _ARAGON_2007_05_LAST_NUMBER = last_number
    elif "Junta Electoral Provincial de Teruel" in text:
        huesca_text, teruel_text = text.split("Junta Electoral Provincial de Teruel")
        huesca_text, last_number = number_candidates(
            huesca_text, UPPER_DON_CANDIDATE_NAME_REGEX, last_number=_ARAGON_2007_05_LAST_NUMBER
        )
        _ARAGON_2007_05_LAST_NUMBER = last_number
        text = huesca_text + "Junta Electoral Provincial de Teruel" + teruel_text
    return text
