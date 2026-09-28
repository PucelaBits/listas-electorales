from ._common import register_fixer


def _murcia_province_fix(text: str) -> str:
    suffix = 1
    text = text.replace("Primera\n", f"MUR-{suffix}\n")
    text = text.replace("PRIMERA\n", f"MUR-{suffix}\n")
    text = text.replace("CIRCUNSCRIPCIÓN N.º 1\n", f"CIRCUNSCRIPCIÓN MUR-{suffix}\n")
    text = text.replace("Segunda\n", f"MUR-{suffix + 1}\n")
    text = text.replace("SEGUNDA\n", f"MUR-{suffix + 1}\n")
    text = text.replace("CIRCUNSCRIPCIÓN N.º 2\n", f"CIRCUNSCRIPCIÓN MUR-{suffix + 1}\n")
    text = text.replace("Tercera\n", f"MUR-{suffix + 2}\n")
    text = text.replace("TERCERA\n", f"MUR-{suffix + 2}\n")
    text = text.replace("CIRCUNSCRIPCIÓN N.º 3\n", f"CIRCUNSCRIPCIÓN MUR-{suffix + 2}\n")
    text = text.replace("Cuarta\n", f"MUR-{suffix + 3}\n")
    text = text.replace("CUARTA\n", f"MUR-{suffix + 3}\n")
    text = text.replace("CIRCUNSCRIPCIÓN N.º 4\n", f"CIRCUNSCRIPCIÓN MUR-{suffix + 3}\n")
    text = text.replace("Quinta\n", f"MUR-{suffix + 4}\n")
    text = text.replace("QUINTA\n", f"MUR-{suffix + 4}\n")
    text = text.replace("CIRCUNSCRIPCIÓN N.º 5\n", f"CIRCUNSCRIPCIÓN MUR-{suffix + 4}\n")
    return text


@register_fixer("murcia", 1983, 5)
def fix_murcia_1983_05(text: str) -> str:
    text = _murcia_province_fix(text)
    return text


@register_fixer("murcia", 1987, 6)
def fix_murcia_1987_06(text: str) -> str:
    text = _murcia_province_fix(text)
    return text


@register_fixer("murcia", 1991, 5)
def fix_murcia_1991_05(text: str) -> str:
    text = _murcia_province_fix(text)
    return text


@register_fixer("murcia", 1995, 5)
def fix_murcia_1995_05(text: str) -> str:
    text = _murcia_province_fix(text)
    return text


@register_fixer("murcia", 1999, 6)
def fix_murcia_1999_06(text: str) -> str:
    text = _murcia_province_fix(text)
    # Facilitate parsing
    text = text.replace("4.º-", "Candidatura número 4.")
    text = text.replace("4º.", "Candidatura número 4.")
    return text


@register_fixer("murcia", 2003, 5)
def fix_murcia_2003_05(text: str) -> str:
    text = _murcia_province_fix(text)
    # Facilitate parsing
    text = text.replace("\n(", " (")
    # Remove footer
    if "Electoral de Zona de Caravaca de la Cruz" in text:
        text = text.split("Electoral de Zona de Caravaca de la Cruz")[0]
    return text


@register_fixer("murcia", 2007, 5)
def fix_murcia_2007_05(text: str) -> str:
    text = _murcia_province_fix(text)
    # Facilitate parsing
    text = text.replace("CANDIDATOS\n", "")
    # Remove footer
    if "Electoral de Zona de Caravaca de la Cruz" in text:
        text = text.split("Electoral de Zona de Caravaca de la Cruz")[0]
    return text


@register_fixer("murcia", 2011, 5)
def fix_murcia_2011_05(text: str) -> str:
    text = _murcia_province_fix(text)
    return text


@register_fixer("murcia", 2015, 5)
def fix_murcia_2015_05(text: str) -> str:
    text = _murcia_province_fix(text)
    return text


@register_fixer("murcia", 2023, 5)
def fix_murcia_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("3. Anuncios", "")
    return text
