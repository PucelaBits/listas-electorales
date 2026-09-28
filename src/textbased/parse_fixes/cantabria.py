from ._common import fix_dona_ocr, register_fixer


@register_fixer("cantabria", 1999, 6)
def fix_cantabria_1999_06(text: str) -> str:
    # Fix OCR
    text = text.replace("1'7. D.", "17. D.")
    text = text.replace("1.0. D.", "10. D.")
    text = fix_dona_ocr(text)
    return text


@register_fixer("cantabria", 2007, 5)
def fix_cantabria_2007_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "37. D. IVAN MARTÍNEZ FERNÁNDEZ",
        "37. D. IVAN MARTÍNEZ FERNÁNDEZ - (INDEPENDIENTE)",
    )
    return text


@register_fixer("cantabria", 2011, 5)
def fix_cantabria_2011_05(text: str) -> str:
    text = text.replace("Orden Nombre y Apellidos\n", "")
    return text
