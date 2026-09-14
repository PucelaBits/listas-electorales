from ._common import register_fixer


def _asturias_province_fix(text: str) -> str:
    text = text.replace("ORIENTE\n", "Astu-1\n")
    text = text.replace("Oriente\n", "Astu-1\n")
    text = text.replace("OCCIDENTE\n", "Astu-2\n")
    text = text.replace("Occidente\n", "Astu-2\n")
    text = text.replace("CENTRO\n", "Astu-3\n")
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
    return text


@register_fixer("asturias", 2003, 5)
def fix_asturias_2003_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2007, 5)
def fix_asturias_2007_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2011, 5)
def fix_asturias_2011_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2012, 3)
def fix_asturias_2012_03(text: str) -> str:
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
