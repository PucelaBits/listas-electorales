from ._common import register_fixer


@register_fixer("ceuta", 2011, 5)
def fix_ceuta_2011_05(text: str) -> str:
    # Remove preamble
    text = text.replace("9.- DOÑA LOURDES", "")
    # Remove footer
    if "Las tarifas vigentes, según acuerdo plenario de " in text:
        return ""
    return text

@register_fixer("ceuta", 2015, 5)
def fix_ceuta_2015_05(text: str) -> str:
    # Remove preamble
    if (
        "Relación definitiva de alumnos beneficiarios de ayudas para" in text
        or "10-. CARMEN RODRIGUEZ VOZMEDIANO" in text
    ):
        return ""
    # Errata (err.pdf)
    text = text.replace("16. Don PATRICIA DIAZ MATEO", "16. Doña PATRICIA DIAZ MATEO")
    text = text.replace("20. Don LIDIA GALAN", "20. Doña LIDIA GALAN")
    text = text.replace(
        "3. Don HOSAIN EL HADDAD ALÍ", "3. Doña HAMAMA BENAASSATI ABDESELAM"
    )
    return text


@register_fixer("ceuta", 2019, 5)
def fix_ceuta_2019_05(text: str) -> str:
    # Remove preamble
    if "HACE PÚBLICO:" in text:
        return ""
    return text


@register_fixer("ceuta", 2023, 5)
def fix_ceuta_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("39.- Edicto de la", "")
    text = text.replace("39.- JUNTA", "")
    return text
