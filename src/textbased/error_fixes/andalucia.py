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


@register_fixer("andalucia", 2000, 3)
def fix_andalucia_2000_03(text: str) -> str:
    if "Instituto Geográfico Nacional" in text:
        # Remove preamble
        return ""
    return text


@register_fixer("andalucia", 2004, 3)
def fix_andalucia_2004_03(text: str) -> str:
    if "CONSEJERIA DE TURISMO Y DEPORTE" in text:
        # Remove preamble
        return ""
    # Remove extra substitute and move it to the missing position
    text = text.replace(
        "Núm.   3.  Juan Tornero Cabezuelo.\n         Núm.   4.  Miguel Angel Soto Blanco.",
        "Núm.   3.  Juan Tornero Cabezuelo.",
    )
    text = text.replace(
        "Núm.   2.  Antonio Ruiz Ortega.",
        "Núm.   2.  Antonio Ruiz Ortega.\n         Núm.   3.  Miguel Angel Soto Blanco.",
    )
    return text


@register_fixer("andalucia", 2008, 3)
def fix_andalucia_2008_03(text: str) -> str:
    text = text.replace(
        "1      Don    Rafael Contreras Fernández\n2      Doña   María Isabel Garrido Asenjo\n3      Don    Antonio Moya Martín\n4      Doña   Montserrat Martín Escobar",
        "1      Don    María Isabel Garrido Asenjo\n2      Don    Antonio Moya Martín\n3      Doña   Montserrat Martín Escobar\n4      Don    Rafael Contreras Fernández",
    )
    text = text.replace(
        "2. PARTIDO SOCIALISTA OBRERO DE ANDALUCÍA (PSOE-A)",
        "2. PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCÍA (PSOE-A)",
    )
    text = text.replace("Rodrigo José González Soler", "Rodrigo José Rodríguez Soler")
    text = text.replace("José Ortega Andrande", "José Ortega Andrade")
    text = text.replace("Sara María Rodríguez Martínez", "Sara María Rodríguez Martín")
    text = text.replace("María Ester Moleón Paiz", "María Esther Moleón Paiz")
    text = text.replace("Jhonatan Frutos Frutos", "Jonatan Frutos Frutos")
    text = text.replace("Rosa Ruiz Escobar", "Rosa María Ruiz Escobar")
    text = text.replace("Gracia Collado Montañero", "Gracia Collado Montanero")
    text = text.replace("ANDALUCIA-ALTERNATIVA (IULV-CA)", "ANDALUCÍA (IULV-CA)")
    text = text.replace("M.ª Luisa Ávila de la Casa", "María Luisa Ávila de la Casa")
    text = text.replace("Carmen Brun Esquilache", "Carmen Brun Esquileche")
    text = text.replace("María Josefa Anes Íñiguez", "María Josefa Anés Íñiguez")
    text = text.replace("Rosa Gema Flores", "Rosa Gemma Flores")
    text = text.replace("Juan de Sosa Montesino", "Juan de Sosa Montesinos")
    return text


@register_fixer("andalucia", 2015, 3)
def fix_andalucia_2015_03(text: str) -> str:
    text = text.replace("Matilde Ortiz Arcas", "Matilde Ortiz Arca")
    text = text.replace(
        "Concepción del Carmen Muñoz Sánchez", "Concepción del Carmelo Muñoz Sánchez"
    )
    text = text.replace(
        "Javier Vicente Del Moral Quevedo", "Juan Vicente Del Moral Quevedo"
    )
    text = text.replace("Nazaret Navarro Todelado", "Nazaret Navarro Toledano")
    return text
