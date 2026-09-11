from ._common import register_fixer


@register_fixer("murcia", 2023, 5)
def fix_murcia_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("3. Anuncios", "")
    return text
