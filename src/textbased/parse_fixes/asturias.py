from ._common import register_fixer


def _asturias_province_fix(text: str) -> str:
    text = text.replace(
        "Circunscripción electoral: Oriente", "Circunscripción electoral: Astu-1"
    )
    text = text.replace(
        "Circunscripción electoral: Occidente", "Circunscripción electoral: Astu-2"
    )
    text = text.replace(
        "Circunscripción electoral: Centro", "Circunscripción electoral: Astu-3"
    )
    return text


@register_fixer("asturias", 2019, 5)
def fix_asturias_2019_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text


@register_fixer("asturias", 2023, 5)
def fix_asturias_2023_05(text: str) -> str:
    text = _asturias_province_fix(text)
    return text
