import re

from ._common import (
    LOWER_CANDIDATE_NAME_REGEX,
    LOWER_DON_CANDIDATE_NAME_REGEX,
    NUMBER_MAP,
    UPPER_CANDIDATE_NAME_REGEX,
    clean_ocr_numbers,
    fix_maria_ocr,
    fix_multiline_candidacy_naming,
    fix_single_inverse_candidacy_fix,
    number_candidates,
    register_fixer,
)


def _canarias_province_fix(text: str) -> str:
    suffix = 1
    text = text.replace("Fuerteventura\n", f"CAN-{suffix}\n")
    text = text.replace("FUERTEVENTURA\n", f"CAN-{suffix}\n")
    text = text.replace("Gran Canaria\n", f"CAN-{suffix + 1}\n")
    text = text.replace("Gran Canaria.\n", f"CAN-{suffix + 1}\n")
    text = text.replace("GRAN CANARIA\n", f"CAN-{suffix + 1}\n")
    text = text.replace("La Gomera\n", f"CAN-{suffix + 2}\n")
    text = text.replace("LA GOMERA\n", f"CAN-{suffix + 2}\n")
    text = text.replace("Lanzarote\n", f"CAN-{suffix + 3}\n")
    text = text.replace("LANZAROTE\n", f"CAN-{suffix + 3}\n")
    text = text.replace("La Palma\n", f"CAN-{suffix + 4}\n")
    text = text.replace("LA PALMA\n", f"CAN-{suffix + 4}\n")
    text = text.replace("PALMAS (LAS)\n", f"CAN-{suffix + 4}\n")
    text = text.replace("Tenerife\n", f"CAN-{suffix + 5}\n")
    text = text.replace("TENERIFE\n", f"CAN-{suffix + 5}\n")
    text = text.replace("El Hierro\n", f"CAN-{suffix + 6}\n")
    text = text.replace("EL HIERRO\n", f"CAN-{suffix + 6}\n")
    return text


@register_fixer("canarias", 1983, 5)
def fix_canarias_1983_05(text: str) -> str:
    text = _canarias_province_fix(text)
    return text


@register_fixer("canarias", 1987, 6)
def fix_canarias_1987_06(text: str) -> str:
    text = _canarias_province_fix(text)
    return text


@register_fixer("canarias", 1991, 6)
def fix_canarias_1991_06(text: str) -> str:
    text = _canarias_province_fix(text)
    return text


@register_fixer("canarias", 1995, 5)
def fix_canarias_1995_05(text: str) -> str:
    text = _canarias_province_fix(text)
    return text


_CANARIAS_1999_06_LAST_NUMBER = 1
_CANARIAS_1999_06_GOMERA_LAST_NUMBER = 1


@register_fixer("canarias", 1999, 6)
def fix_canarias_1999_06(text: str) -> str:
    # Remove preamble
    text = text.replace("El Presidente José Antonio González González", "")
    if "RAQUEL MARTÍNEZ MAZÓN SECRETARIA DE LA" in text:
        text = text.split("RAQUEL MARTÍNEZ MAZÓN SECRETARIA DE LA")[-1]
    text = text.replace(
        "CIRCUNSCRIPCIÓN DE LA GOMERA PARA LAS", "CIRCUNSCRIPCIÓN DE LA GOMERA\n"
    )
    text = text.replace(
        "CIRCUNSCRIPCIÓN DE EL HIERRO PARA LAS", "CIRCUNSCRIPCIÓN DE EL HIERRO\n"
    )
    text = text.replace(
        "CIRCUNSCRIPCIÓN DE LA PALMA PARA LAS", "CIRCUNSCRIPCIÓN DE LA PALMA\n"
    )
    text = text.replace(
        "CIRCUNSCRIPCIÓN DE TENERIFE PARA LAS", "CIRCUNSCRIPCIÓN DE TENERIFE\n"
    )
    text = _canarias_province_fix(text)
    text = text.replace("N2 NOM", "NOM")
    text = text.replace("CANDIDATURA NY ", "CANDIDATURA N ")
    text = text.replace("CANDIDATURA N9 ", "CANDIDATURA N ")
    text = text.replace("CANDIDATURA Nf ", "CANDIDATURA N ")
    text = text.replace("CANDIDATURA N2 ", "CANDIDATURA N ")
    text = text.replace("PARTFEDER JAGRUP", "PART/FEDER/AGRUP")
    text = text.replace("PART.FEDER JAGRUP", "PART/FEDER/AGRUP")
    text = text.replace("PART.FEDER.JAGRUP", "PART/FEDER/AGRUP")
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA N {number_text}\n", f"CANDIDATURA N {number}\n"
        )
    text = fix_multiline_candidacy_naming(text)
    # Fix OCR
    text = text.replace(". Independiente", "")
    text = text.replace("Y ánez", "Yánez")
    text = text.replace("Díia.", "Dña.")
    text = text.replace("Día.", "Dña.")
    text = text.replace("J2 .- D.\n", "J2.- D. ")
    text = text.replace("UNIÓN CENTRISTA-CENTRO DEMOCRÁTICO Y SO-\n", "UNIÓN CENTRISTA-CENTRO DEMOCRÁTICO Y SO")
    text = clean_ocr_numbers(text)
    text = fix_single_inverse_candidacy_fix(text)
    global _CANARIAS_1999_06_LAST_NUMBER
    text, _CANARIAS_1999_06_LAST_NUMBER = number_candidates(
        text,
        LOWER_DON_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_1999_06_LAST_NUMBER,
    )
    global _CANARIAS_1999_06_GOMERA_LAST_NUMBER
    text, _CANARIAS_1999_06_GOMERA_LAST_NUMBER = number_candidates(
        text,
        LOWER_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_1999_06_GOMERA_LAST_NUMBER,
    )
    return text


@register_fixer("canarias", 2003, 5)
def fix_canarias_2003_05(text: str) -> str:
    # TODO: Errata (err.pdf)
    # Remove preamble
    if "que no trasciendan del ámbito de este Centro" in text:
        return ""
    # Remove footer
    if "Errores cometidos por esta Junta en la publicación" in text:
        text = text.split("Errores cometidos por esta Junta en la publicación")[0]
    text = _canarias_province_fix(text)
    # Fixes for parsing
    text = fix_multiline_candidacy_naming(text)
    # Fix missing candidacy
    text = text.replace(
        "Candidatura núm. 11: PARTIDO",
        "Candidatura núm. 10: RELLENO\nNO PROCLAMADA\nCandidatura núm. 11: PARTIDO",
    )
    return text


@register_fixer("canarias", 2007, 5)
def fix_canarias_2007_05(text: str) -> str:
    # TODO: err_3.pdf
    # Errata (err.pdf)
    text = text.replace(
        "D. Juan Carlos Navarro Pérez",
        "D. Juan Carlos Navarro Pérez (Independiente)",
    )
    text = text.replace("Pedro Jesús Betancor Machón", "Pedro Jesús Betancor Machín")
    text = text.replace("Germán Briton Martín", "Germán Brito Martín")
    text = text.replace("Félix Andrés Gonzalo Lorenzo", "Félix Andrés González Lorenzo")
    # Fixes for parsing
    text = fix_multiline_candidacy_naming(text)
    text = _canarias_province_fix(text)
    text = text.replace("Nº Nombre y apellidos Partido o\nFederación", "")
    text = text.replace("NACIONALISTA\n", "NACIONALISTA ")
    return text


_CANARIAS_2011_05_LAST_NUMBER = None


@register_fixer("canarias", 2011, 5)
def fix_canarias_2011_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "Doña Venancio Pérez Hernández", "Doña Venancia Pérez Hernández"
    )
    text = text.replace("Noela García Ramos", "Noelia García Ramos")
    text = text.replace("Siglas: Nca", "Siglas: NCa")
    text = text.replace(
        "6 Don \nFeliz Andrés \nGonzález \nLorenzo",
        "6 Don \nFélix Andrés \nGonzález \nLorenzo",
    )
    text = text.replace(
        "1 Doña\nRosa\nRivero\nAbreu",
        "1 Doña\nRosi\nRivero\nAbreu",
    )
    text = text.replace(
        "Arturo Mario\nMéndez\nLloret",
        "Arturo Mario\nMéndez\nLlorens",
    )
    text = text.replace("Iglesias\nSangil", "Iglesias\nSan Gil")
    text = text.replace(
        "Anotomía Mª\nVera\nPerera",
        "Antonia María\nVera\nPerera",
    )
    # Fix OCR
    text = text.replace(".Marcuño", "Marcuño")
    text = text.replace("G11l", "Gil")
    text = text.replace("Aracel1", "Araceli")
    text = text.replace("BlázquezVidal", "Blázquez Vidal")
    text = text.replace("CarmeloRamírezÁlvarez", "Carmelo Ramírez Álvarez")
    text = text.replace("SantanaGarcía", "Santana García")
    text = text.replace("Nleves", "Nieves")
    text = text.replace("lone", "Ione")
    text = text.replace("PinoGonzález", "Pino González")
    text = text.replace("JoséCruz", "José Cruz")
    text = text.replace("JOSé", "José")
    text = text.replace(
        "Doña Patricia 1. García Reyes", "Doña Patricia I. García Reyes"
    )
    text = text.replace(
        "Doña Maria del Rosario WMarl Saro Hernández González",
        "Doña Maria del Rosario Hernández González",
    )
    text = text.replace("don Antonio F", "Don Antonio F")
    text = text.replace(
        "Doña Magdalena de la A Cabrera", "Doña Magdalena de la A. Cabrera"
    )
    text = fix_maria_ocr(text)
    text = text.replace("7\nCandidatura número:\n", "Candidatura número: 7\n")
    text = text.replace(
        "Don David Peñas López\nCandidatura número:\nDenominación: LOS VERDES",
        "Don David Peñas López\nCandidatura número: 5\nDenominación: LOS VERDES",
    )
    text = text.replace(
        "ES\nCandidatura número:\nDenominación: LOS VERDES",
        "ES\nCandidatura número: 5\nDenominación: LOS VERDES",
    )
    text = text.replace(
        "ES\nCandidatura número:\nDenominación: NUEVA CANARIAS",
        "ES\nCandidatura número: 7\nDenominación: NUEVA CANARIAS",
    )
    text = text.replace(
        "Candidatura número:\nDenominación: LOS VERDES",
        "Candidatura número: 4\nDenominación: LOS VERDES",
    )
    text = text.replace(
        "Candidatura número:\nDenominación: PARTIDO POPULAR",
        "Candidatura número: 2\nDenominación: PARTIDO POPULAR",
    )
    text = text.replace(
        "ASAMBLEAS MUNICIPALES DE FUERTEVENTURA-NUEVA FUERTEVENTURA\n",
        "ASAMBLEAS MUNICIPALES DE FUERTEVENTURA-NUEVA FUERTEVENTURA ",
    )
    text = _canarias_province_fix(text)
    text = fix_multiline_candidacy_naming(text)
    global _CANARIAS_2011_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        LOWER_DON_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_2011_05_LAST_NUMBER,
    )
    _CANARIAS_2011_05_LAST_NUMBER = last_number
    return text


_CANARIAS_2015_05_LAST_NUMBER = None


@register_fixer("canarias", 2015, 5)
def fix_canarias_2015_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "FRANCISCO GUZMAN RODRIGUEZ",
        "FRANCISCO GUZMAN RODRIGUEZ REYES",
    )
    text = text.replace(
        "NATALIA CURBELO CABRERO",
        "NATALIA CURBELO CABRERA",
    )
    # Other fixes to facilitate parsing
    text = fix_maria_ocr(text, upper=True)
    text = text.replace("PABLO l. GARCÍA HERNÁNDEZ", "PABLO I. GARCÍA HERNÁNDEZ")
    text = text.replace(
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-\n",
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-",
    )
    text = text.replace(
        "INICIATIVA POR EL HIERRO-IZQUIERDA UNIDA CANARIA-\n",
        "INICIATIVA POR EL HIERRO-IZQUIERDA UNIDA CANARIA-",
    )
    text = text.replace(
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-UNIDAD DEL\n",
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-UNIDAD DEL ",
    )
    text = _canarias_province_fix(text)
    global _CANARIAS_2015_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        UPPER_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_2015_05_LAST_NUMBER,
    )
    _CANARIAS_2015_05_LAST_NUMBER = last_number
    return text


_CANARIAS_2019_05_LAST_NUMBER = None


@register_fixer("canarias", 2019, 5)
def fix_canarias_2019_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA (CCa)",
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA-PARTIDO NACIONALISTA CANARIO (CCa-PNC)",
    )
    # Facilitate parsing
    text = text.replace(
        "Circunscripción electoral: Autonómica", "Circunscripción electoral: Canarias"
    )
    text = text.replace(
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA (ANC) Y UNIDAD\n",
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA (ANC) Y UNIDAD ",
    )
    text = text.replace(
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA ANC y UNIDAD\n",
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA ANC y UNIDAD ",
    )
    text = text.replace("5. JUNTA ELECTORAL", "JUNTA ELECTORAL")
    text = text.replace("MARÍA INMACULADA Pl MULET", "MARÍA INMACULADA PI MULET")
    text = text.replace("(PODEMOS\n", "(PODEMOS)\n")
    text = fix_maria_ocr(text, upper=True)
    # Fix missing numbers
    global _CANARIAS_2019_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        UPPER_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_2019_05_LAST_NUMBER,
    )
    _CANARIAS_2019_05_LAST_NUMBER = last_number
    text = _canarias_province_fix(text)
    return text


_CANARIAS_2023_05_LAST_NUMBER = None


@register_fixer("canarias", 2023, 5)
def fix_canarias_2023_05(text: str) -> str:
    # TODO: err.pdf
    # Remove weird duplication
    if "MATÍAS HERNÁNDEZ PADRÓN" in text:
        text = text.replace(
            "KEVIN TOMÁS QUEVEDO MARTÍN \n \nCandidatura núm.: 10. CONTIGO SOMOS DEMOCRACIA (CONTIGO) \n \nNO PROCLAMADA \n \nCandidatura núm.: 11. AHORA TÚ (AT) \n",
            "",
        )
    elif "ANTONIO MARÍN MUÑOZ" in text:
        text = text.replace(
            "\nSAÚL GÓMEZ ALBEROLA \nNAIRA MARRERO JAÉN \n \nSuplentes \nALEXANDER VELÁZQUEZ DÍAZ \nMARÍA DEL CARMEN LLANOS GAVIRIA \nRAMÓN TRUJILLO MORALES \n \nCandidatura núm.: 14. PAIS CON GESTORES (PAIS CON GESTORES) \n",
            "",
        )
    # Fix missing numbers
    global _CANARIAS_2023_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        UPPER_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_2023_05_LAST_NUMBER,
    )
    _CANARIAS_2023_05_LAST_NUMBER = last_number

    return text
