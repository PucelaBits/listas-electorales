from ._common import NUMBER_MAP, clean_ocr_numbers, register_fixer


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
