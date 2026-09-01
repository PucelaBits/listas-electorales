from ._common import clean_ocr_text, register_fixer


@register_fixer("andalucia", 1994, 6)
def fix_andalucia_1994_06(text: str) -> str:
    if "EXPOSICION DE MOTIVOS" in text:
        # Remove preamble
        return ""
    text = text.replace(
        "PROVINCIA DE*MALAGA\n\n        Núm. 1.- PARTIDO POPULAR (P.P.)",
        "PROVINCIA DE MALAGA \nNúm. 1. PARTIDO POPULAR DE ANDALUCIA (P.P.)",
    )
    text = text.replace("Rafael GraCia Contreras", "Rafael García Contreras")
    text = text.replace("Manuel Ruiz Madruga", "Miguel Ruiz Madruga")
    text = text.replace("Peñuelas Cancharro", "Peñuelas Lancharro")
    # Remove extra substitutes
    text = text.replace("Núm. 4. Doña María Mercedes Fernández Olivares.", "")
    text = text.replace("Núm. 5. Don José Garrido Porras.", "")
    # Add missing substitutes (just replicate the last substitute to the missing position)
    text = text.replace("1. Don Mario García Guillén", "1. Don Mario García Guillén\n2. Don Mario García Guillén\n3. Don Mario García Guillén")
    text = text.replace("Núm. .- PARTIDO POPULAR (P.P.)", "Núm. 1. PARTIDO POPULAR (P.P.)")
    # Hardcoded fixes for OCR
    text = text.replace("1.-.PARTIDO POPULAR", "1. PARTIDO POPULAR")
    text = text.replace("1'. Don Mariano JuncoGonzález", "1. Don Mariano Junco González")
    text = text.replace("5.- IZQUIERDA UNIDA LOS VERDES-C(INVOCATORIA POR ANDALUCIA", "5.- IZQUIERDA UNIDA LOS VERDES-CONVOCATORIA POR ANDALUCIA")
    text = text.replace(r"i\lúrn. 5. Don Manuel Jesús González. Gamerá.", "Núm. 5. Don Manuel Jesús González Gamero.")
    text = text.replace("Núm. 1-0. Doña María del Mar García Andrés.", "Núm. 10. Doña María del Mar García Andrés.")
    text = text.replace("Núm. 2. Doña María de la Paz Llavero del Pozo", "Núm. 3. Doña María de la Paz Llavero del Pozo")
    text = text.replace("Don Manuel Rodríguez Gamiz", "5. Don Manuel Rodríguez Gamiz")
    text = text.replace("Don Francilco Lorenzo Cuevas", "Don Francisco Lorenzo Cuevas")
    text = text.replace("5, Don Joaquín Jesús Galán Pérez", "5. Don Joaquín Jesús Galán Pérez")
    text = text.replace("7.? Don Francisco Martín Rodríguez", "7. Don Francisco Martín Rodríguez")
    text = text.replace("1.2.  Don José Selma García", "12. Don José Selma García")
    text = text.replace("Núm. J. Don Juan Oleda Sanz", "Núm. 1. Don Juan Oleda Sanz")
    text = text.replace("Suplerites", "Suplentes")
    text = text.replace("Sliplentes", "Suplentes")
    text = text.replace("-Suplentes", "Suplentes")
    text = text.replace("?odríguez", "Rodríguez")
    text = clean_ocr_text(text)
    return text


@register_fixer("andalucia", 1996, 3)
def fix_andalucia_1996_03(text: str) -> str:
    if "CONSEJERIA DE TRABAJO Y ASUNTOS SOCIALES" in text:
        # Remove preamble
        return ""
    return text


@register_fixer("andalucia", 2000, 3)
def fix_andalucia_2000_03(text: str) -> str:
    if "Instituto Geográfico Nacional" in text:
        # Remove preamble
        return ""
    # Not proclaimed
    text = text.replace("3.  PARTIDO POSITIVISTA CRISTIANO (PPCr)", "")
    # Missing substitute (just replicate the last substitute to the missing position)
    text = text.replace(
        "Núm.  2.  Remedios Moreno Gómez.",
        "Núm.  2.  Remedios Moreno Gómez.\n         Núm.  3.  Remedios Moreno Gómez.",
    )
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
