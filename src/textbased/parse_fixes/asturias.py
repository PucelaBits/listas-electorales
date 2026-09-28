from ._common import clean_ocr_numbers, register_fixer


def _asturias_province_fix(text: str) -> str:
    text = text.replace("ORIENTE\n", "Astu-1\n")
    text = text.replace("ORIENTAL\n", "Astu-1\n")
    text = text.replace("ORIENTAL.\n", "Astu-1\n")
    text = text.replace("Oriente\n", "Astu-1\n")
    text = text.replace("OCCIDENTE\n", "Astu-2\n")
    text = text.replace("OCCIDENTAL\n", "Astu-2\n")
    text = text.replace("OCCIDENTAL.\n", "Astu-2\n")
    text = text.replace("Occidente\n", "Astu-2\n")
    text = text.replace("CENTRO\n", "Astu-3\n")
    text = text.replace("CENTRAL\n", "Astu-3\n")
    text = text.replace("CENTRAL.\n", "Astu-3\n")
    text = text.replace("Centro\n", "Astu-3\n")
    return text


@register_fixer("asturias", 1983, 5)
def fix_asturias_1983_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 1987, 6)
def fix_asturias_1987_06(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 1991, 5)
def fix_asturias_1991_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 1995, 5)
def fix_asturias_1995_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 1999, 6)
def fix_asturias_1999_06(text: str) -> str:
    text = _asturias_province_fix(text)
    text = text.replace("Candidatos\n", "")
    text = text.replace("CIRCUNSCRIPCION\n", "CIRCUNSCRIPCIÓN ")
    text = text.replace("Stiplentes", "Suplentes")
    # Fix OCR errors
    text = text.replace("ServandoFernandezAmado", "Servando Fernández Amado")
    text = clean_ocr_numbers(text)
    return text


@register_fixer("asturias", 2003, 5)
def fix_asturias_2003_05(text: str) -> str:
    text = _asturias_province_fix(text)
    text = text.replace("Candidatos\n", "")
    text = text.replace("CIRCUNSCRIPCION\n", "CIRCUNSCRIPCIÓN ")
    # Fix OCR
    text = text.replace("9, ", "9. ")
    text = text.replace("25, ", "25. ")
    text = text.replace("1, ", "1. ")
    text = text.replace("23, ", "23. ")
    text = clean_ocr_numbers(text)
    # Fix candidates
    text = text.replace(
        "2. Encarnación González Martínez", "3. Encarnación González Martínez"
    )
    # Remove unexpected candidate
    text = text.replace("21. Nelly Azucena Carabajo Rivas", "")
    return text


@register_fixer("asturias", 2007, 5)
def fix_asturias_2007_05(text: str) -> str:
    text = text.replace("Candidatos\n", "")
    text = text.replace("CIRCUNSCRIPCION\n", "CIRCUNSCRIPCION ELECTORAL ")
    text = _asturias_province_fix(text)
    # Fix missing candidacy
    text = text.replace(
        "11. Convergencia Democrática Asturiana (CDAS)",
        "Candidatura número 10. RELLENO\nNO PROCLAMADA\n11. Convergencia Democrática Asturiana (CDAS)",
    )
    return text


@register_fixer("asturias", 2011, 5)
def fix_asturias_2011_05(text: str) -> str:
    text = text.replace("Candidatos:\n", "")
    text = text.replace("CIRCUNSCRIPCIÓN ", "CIRCUNSCRIPCIÓN ELECTORAL ")
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2012, 3)
def fix_asturias_2012_03(text: str) -> str:
    text = text.replace("Candidatos\n", "")
    text = text.replace("CIRCUNSCRIPCIÓN ", "CIRCUNSCRIPCIÓN ELECTORAL ")
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2015, 5)
def fix_asturias_2015_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2019, 5)
def fix_asturias_2019_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2023, 5)
def fix_asturias_2023_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text
