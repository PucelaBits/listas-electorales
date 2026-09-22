import re

from ._common import fix_multiline_candidacy_naming, register_fixer


@register_fixer("la_rioja", 2003, 5)
def fix_la_rioja_2003_05(text: str) -> str:
    text = fix_multiline_candidacy_naming(text)
    text = re.sub(r"^Símbolo:\n.+$", "", text, flags=re.MULTILINE)
    return text


@register_fixer("la_rioja", 2011, 5)
def fix_la_rioja_2011_05(text: str) -> str:
    # Remove footer
    if (
        "Publicación de candidaturas, fase proclamación, elecciones Locales 2011"
        in text
    ):
        return text.split(
            "Publicación de candidaturas, fase proclamación, elecciones Locales 2011"
        )[0]
    return text


@register_fixer("la_rioja", 2015, 5)
def fix_la_rioja_2015_05(text: str) -> str:
    # Fix missing spaces
    text = text.replace("￿", " ")
    return text


@register_fixer("la_rioja", 2019, 5)
def fix_la_rioja_2019_05(text: str) -> str:
    # Fix missing spaces
    text = text.replace("￿", " ")
    return text


@register_fixer("la_rioja", 2023, 5)
def fix_la_rioja_2023_05(text: str) -> str:
    # Fix missing spaces
    text = text.replace("￿", " ")
    return text
