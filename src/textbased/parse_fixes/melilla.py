from ._common import register_fixer


@register_fixer("melilla", 2019, 5)
def fix_melilla_2019_05(text: str) -> str:
    # TODO: err.pdf
    text = text.replace(
        "26. Suplentes\n27. Rosa María Montero Madrid\n28. Oliverio Sánchez Vargas\n29. María Consuelo Guerra Muñoz",
        "Suplentes\n1. Rosa María Montero Madrid\n2. Oliverio Sánchez Vargas\n3. María Consuelo Guerra Muñoz",
    )
    text = text.replace(
        "Candidatura núm. 8: COALICION POR MELILLA (CPM)\nNo proclamada\nCandidatura núm. 9: AHORA MELILLA (AHORA MELILLA)\nNo proclamada\n",
        "",
    )
    return text


@register_fixer("melilla", 2023, 5)
def fix_melilla_2023_05(text: str) -> str:
    # Remove preamble
    text = text.replace("120. PROCLAMACIÓN CANDIDATURAS", "")
    return text
