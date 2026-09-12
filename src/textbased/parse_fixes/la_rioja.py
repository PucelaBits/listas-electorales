from ._common import register_fixer


@register_fixer("la_rioja", 2023, 5)
def fix_la_rioja_2023_05(text: str) -> str:
    # Fix missing spaces
    text = text.replace("￿", " ")
    return text
