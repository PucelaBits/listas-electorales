import re

from ._common import register_fixer


# BOJA 17.5.1994:
#   err_1 (Málaga) -> "1. Partido Popular (P.P.)" -> "1. Partido Popular de Andalucía (P.P.)"
#   err_2 (Córdoba) -> "Don Rafael Gracia Contreras" -> "García Contreras" (typo capital)
#                     -> "Don Manuel Ruiz Madruga"   -> "Don Miguel Ruiz Madruga"
#                     -> "Don Joaquín Peñuelas Cancharro" -> "Don Joaquín Peñuelas Lancharro"
@register_fixer("andalucia", 1994, 6)
def fix_andalucia_1994_06(text: str) -> str:
    # err_1: only the PP line right under "PROVINCIA DE*MALAGA" must be renamed;
    # other provinces legitimately list "PARTIDO POPULAR (P.P.)".
    text = text.replace(
        "PROVINCIA DE*MALAGA \nNúm. 1.- PARTIDO POPULAR (P.P.)",
        "PROVINCIA DE*MALAGA \nNúm. 1.- PARTIDO POPULAR DE ANDALUCIA (P.P.)",
    )
    # err_2 (Córdoba). The printed name carries a stray mid-word capital "GraCia".
    text = text.replace("Rafael GraCia Contreras", "Rafael García Contreras")
    text = text.replace("Manuel Ruiz Madruga", "Miguel Ruiz Madruga")
    text = text.replace("Peñuelas Cancharro", "Peñuelas Lancharro")
    return text


# BOJA 37, err.pdf. One line per "Donde dice / Debe decir".
# NOTE: NOT POSSIBLE via text fix: Granada "4. Convergencia Andaluza (CAnda)" Suplentes
#   order 1-4 listed as [Contreras Fernández, Garrido Asenjo, Moya Martín, Martín Escobar]
#   but must be [Garrido Asenjo, Moya Martín, Martín Escobar, Contreras Fernández];
#   the fix swaps candidates across four "order + honorific + name" line groups that are
#   individually identical in shape, so a per-page text substitution cannot reorder them
#   uniquely (a candidate with a very specific name could be moved, but the parser
#   assigns order from the "N" line, which would also have to move).
ANDALUCIA_2008_03_REPLACEMENTS = {
    # Original literals
    "Rodrigo José González Soler": "Rodrigo José Rodríguez Soler",
    "José Ortega Andrande": "José Ortega Andrade",
    "Sara María Rodríguez Martínez": "Sara María Rodríguez Martín",
    "Doña\nHugo Cañellas Ávila": "Don\nHugo Cañellas Ávila",
    "María Ester Moleón Paiz": "María Esther Moleón Paiz",
    "Jhonatan Frutos Frutos": "Jonatan Frutos Frutos",
    "Rosa Ruiz Escobar": "Rosa María Ruiz Escobar",
    "Gracia Collado Montañero": "Gracia Collado Montanero",
    "M.ª Luisa Ávila de la Casa": "María Luisa Ávila de la Casa",
    "Brun Esquilache": "Brun Esquileche",
    "María Josefa Anes Íñiguez": "María Josefa Anés Íñiguez",
    "Rosa Gema Flores": "Rosa Gemma Flores",
    "de Sosa Montesino": "de Sosa Montesinos",
    # Expanded regex variations to enable a single dictionary pass
    "2. PARTIDO SOCIALISTA OBRERO DE ANDALUCIÁ (PSOE-A)": "2. PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCÍA (PSOE-A)",
    "2. PARTIDO SOCIALISTA OBRERO DE ANDALUCÍA (PSOE-A)": "2. PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCÍA (PSOE-A)",
    "ANDALUCIA-ALTERNATIVA (IULV-CA)": "ANDALUCÍA (IULV-CA)",
    "ANDALUCÍA-ALTERNATIVA (IULV-CA)": "ANDALUCÍA (IULV-CA)",
}
P_ANDALUCIA_2008_03_ALL = re.compile(
    "|".join(map(re.escape, ANDALUCIA_2008_03_REPLACEMENTS.keys()))
)


@register_fixer("andalucia", 2008, 3)
def fix_andalucia_2008_03(text: str) -> str:
    # All substitutions (including previous regexes) happen in a single pass
    return P_ANDALUCIA_2008_03_ALL.sub(
        lambda m: ANDALUCIA_2008_03_REPLACEMENTS[m.group(0)], text
    )


# BOJA 49, err.pdf.
@register_fixer("andalucia", 2015, 3)
def fix_andalucia_2015_03(text: str) -> str:
    # Granada PP nº 10: Ortiz Arcas -> Ortiz Arca
    text = text.replace("Doña Matilde Ortiz Arcas", "Doña Matilde Ortiz Arca")
    # Granada PP 3.ª suplente: del Carmen -> del Carmelo
    text = text.replace(
        "Concepción del Carmen Muñoz Sánchez",
        "Concepción del Carmelo Muñoz Sánchez",
    )
    # Jaén PA tit. 9: Javier -> Juan (PDF prints it with a capital "Del")
    text = text.replace(
        "Javier Vicente Del Moral Quevedo", "Juan Vicente Del Moral Quevedo"
    )
    # Jaén CILUS tit. 6: Todelado -> Toledano
    text = text.replace("Nazaret Navarro Todelado", "Nazaret Navarro Toledano")
    return text
