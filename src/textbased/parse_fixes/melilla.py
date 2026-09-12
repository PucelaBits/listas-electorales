from ._common import register_fixer


@register_fixer("melilla", 2023, 5)
def fix_melilla_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("120. PROCLAMACIÓN CANDIDATURAS", "")
    return text
