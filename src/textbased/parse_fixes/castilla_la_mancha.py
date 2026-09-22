import re

from ._common import (
    NUMBER_MAP,
    UPPER_CANDIDATE_REGEX,
    clean_ocr_numbers,
    number_candidates,
    register_fixer,
)

_CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER = 1


@register_fixer("castilla_la_mancha", 2003, 5)
def fix_castilla_la_mancha_2003_05(text: str) -> str:
    # Remove footer
    if "Y para que así co" in text:
        text = text.split("Y para que así co")[0]
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}:\n", f"CANDIDATURA NÚM. {number}:"
        )
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}\n", f"CANDIDATURA NÚM. {number}:\n"
        )
    # Facilitate parsing
    text = text.replace("IZQUIERDA UNIDA - IZ IERDA D ILLA- MANCHA\n(1.U.)", "Candidatura núm. 3: IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA-LA MANCHA (I.U.)")
    text = text.replace("IERRA COMUNERA-PARTID IONALIST", "Candidatura núm. 6: TIERRA COMUNERA-PARTIDO NACIONALISTA CASTELLANO")
    # Fix OCR
    text = text.replace("23 de diciembre Electoral", "")
    text = text.replace("N9 3. .- Adolfo Suárez lllana.", "1. Adolfo Suárez Illana.")
    global _CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER
    # Ciudad Real fix
    for page in range(6373, 6379 + 1):
        if str(page) in text:
            text = text.replace("1.- PARTIDO POPULAR", "Candidatura núm. 1: PARTIDO POPULAR")
            text = text.replace("2.- PARTIDO SOCIALISTA OBRERO ESPAÑOL (PSOE", "Candidatura núm. 2: PARTIDO SOCIALISTA OBRERO ESPAÑOL (PSOE")
            text = text.replace("3.- LAFALANGE", "Candidatura núm. 3: LA FALANGE")
            text = text.replace("4.- TIERRA COMUNERA", "Candidatura núm. 4: TIERRA COMUNERA")
            text = text.replace("5.- UNIDAD", "Candidatura núm. 5: UNIDAD")
            text = text.replace("IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA-LA MANCHA", "Candidatura núm. 6: IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA-LA MANCHA")
            text = text.replace("7.- IZQUIERDA", "Candidatura núm. 7: IZQUIERDA")
            text, _CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER = number_candidates(
                text,
                UPPER_CANDIDATE_REGEX,
                last_number=_CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER,
            )
    text = clean_ocr_numbers(text)
    return text


@register_fixer("castilla_la_mancha", 2007, 5)
def fix_castilla_la_mancha_2007_05(text: str) -> str:
    text = text.replace("PROVINCIAL\n", "PROVINCIAL ")
    text = text.replace("Provincial de\n", "Provincial de ")
    text = text.replace("IZQUIERDA\n", "IZQUIERDA ")
    text = text.replace("próximo\n", "próximo ")
    text = text.replace("Guadala-\n", "Guadala")
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}:\n", f"CANDIDATURA NÚM. {number}:"
        )
    # Fix OCR
    text = clean_ocr_numbers(text)
    text = text.replace("3 DON MANUEL HERNÁNDEZ", "1. DON MANUEL HERNÁNDEZ")
    text = text.replace("4 DON GREGORIO SÁNCHEZ", "1. DON GREGORIO SÁNCHEZ")
    text = text.replace("da. DON JESÚS FERNÁNDEZ", "11. DON JESÚS FERNÁNDEZ")
    text = text.replace("N3 LA FALANGE", "Candidatura núm. 3. LA FALANGE")
    return text


@register_fixer("castilla_la_mancha", 2011, 5)
def fix_castilla_la_mancha_2011_05(text: str) -> str:
    text = text.replace(
        "4. DON DAVID PARDO MOYA\n5. DOÑA MARIA ELENA ESCOBAR GUERRERO\n6. DON PABLO JESUS CANO DURAN",
        "1. DON DAVID PARDO MOYA\n2. DOÑA MARIA ELENA ESCOBAR GUERRERO\n3. DON PABLO JESUS CANO DURAN",
    )
    return text


@register_fixer("castilla_la_mancha", 2015, 5)
def fix_castilla_la_mancha_2015_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "Candidatura núm.: 9. PARTIDO CASTELLANO (PCAS)",
        "Candidatura núm.: 9. PARTIDO CASTELLANO-UNIDAD CASTELLANA (PCAS-UdCA)",
    )
    return text


@register_fixer("castilla_la_mancha", 2023, 5)
def fix_castilla_la_mancha_2023_05(text: str) -> str:
    # Fix dangling suplentes
    text = text.replace("SUPLENTES:\nY para que conste", "")
    return text
