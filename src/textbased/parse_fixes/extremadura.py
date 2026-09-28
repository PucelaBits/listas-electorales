from ._common import register_fixer


@register_fixer("extremadura", 1995, 5)
def fix_extremadura_1995_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("JOSE BAZQUEZ ALVAREZ", "JOSE VAZQUEZ ALVAREZ")
    return text


@register_fixer("extremadura", 1999, 6)
def fix_extremadura_1999_06(text: str) -> str:
    # Remove preamble
    if "siguientes candidatos un puesto y quedando" in text:
        text = "JUNTA ELECTORAL PROVINCIAL DE BADAJOZ\n" + text.split("siguientes candidatos un puesto y quedando")[-1]
    text = text.replace("CACERES", "CÁCERES")
    # Fix random errata
    text = text.replace("l.-", "1.-")
    return text


@register_fixer("extremadura", 2003, 5)
def fix_extremadura_2003_05(text: str) -> str:
    # Remove preamble
    if "ampliación al acuerdo de la Junta Electoral" in text:
        text = (
            "JUNTA ELECTORAL DE BADAJOZ"
            + text.split("ampliación al acuerdo de la Junta Electoral")[-1]
        )
    return text
