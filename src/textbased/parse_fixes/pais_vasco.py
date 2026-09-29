from ._common import fill_missing_numbers, register_fixer


def _fix_substitutes_declaration(text: str) -> str:
    text = text.replace("ORDEZKOAK/SUPLENTES", "SUPLENTES")
    text = text.replace("ORDEZKAOAK/SUPLENTES", "SUPLENTES")
    text = text.replace("ORDEZKOAK/ SUPLENTES", "SUPLENTES")
    text = text.replace("ORDEZKOAK / SUPLENTES", "SUPLENTES")
    text = text.replace("ORDEZKOAK /SUPLENTES", "SUPLENTES")
    text = text.replace("Ordezkoak / Suplentes", "SUPLENTES")
    return text


@register_fixer("pais_vasco", 1986, 11)
def fix_pais_vasco_1986_11(text: str) -> str:
    text = _fix_substitutes_declaration(text)
    return text


@register_fixer("pais_vasco", 1994, 10)
def fix_pais_vasco_1994_10(text: str) -> str:
    text = _fix_substitutes_declaration(text)
    return text


@register_fixer("pais_vasco", 1998, 10)
def fix_pais_vasco_1998_10(text: str) -> str:
    # Remove preamble
    if "en su reunión del día de la fecha de" in text:
        return "JUNTA ELECTORAL DEL TERRITORIO HISTÓRICO DE ÁLAVA"
    if "tagaiak honako hauek direla:" in text:
        text = "JUNTA ELECTORAL DEL TERRITORIO HISTÓRICO DE BIZKAIA" + text.split("tagaiak honako hauek direla:")[-1]
    text = text.replace("Junta Electoral del Territorio\n", "Junta Electoral del Territorio de ")
    text = text.replace("de la Junta Electoral del Territorio de Álava.\na 28 de septiembre 1998.", "")
    text = text.replace("N.º 185 ZK", "")
    text = text.replace("5.– 1.– CARLOS", "1.- CARLOS")
    text = _fix_substitutes_declaration(text)
    # Facilitate parsing
    text = text.replace("4.– IZQUIERDA UNIDA", "Candidatura núm. 4: IZQUIERDA UNIDA")
    text = text.replace("6.– PARTIDO HUMANISTA", "Candidatura núm. 6: PARTIDO HUMANISTA")
    text = text.replace("TERESA\n", "TERESA ")
    return text


@register_fixer("pais_vasco", 2001, 5)
def fix_pais_vasco_2001_05(text: str) -> str:
    text = _fix_substitutes_declaration(text)
    text = text.replace("\n(", " (")
    # Add missing candidacy
    text = text.replace("2001\n7.– ASKATASUNA", "2001\nCandidatura núm. 6: RELLENO\nNO PROCLAMADA\n7.– ASKATASUNA")
    text = text.replace("8.– PARTIDO DEL KARMA DEMOCRATICO (PKD)", "Candidatura núm. 7: RELLENO\nNO PROCLAMADA\n8.– PARTIDO DEL KARMA DEMOCRATICO (PKD)")
    return text


@register_fixer("pais_vasco", 2005, 4)
def fix_pais_vasco_2005_04(text: str) -> str:
    text = _fix_substitutes_declaration(text)
    # Facilitate parsing
    text = text.replace(
        "BIZKAIKO LURRALDE HISTORIKOKO JUNTA ELECTORAL DEL TERRITORIO",
        "JUNTA ELECTORAL DEL TERRITORIO HISTÓRICO DE BIZKAIA",
    )
    text = text.replace(
        "GIPUZKOAKO KONDAIRA-LURRALDEKO JUNTA ELECTORAL DEL TERRITORIO",
        "JUNTA ELECTORAL DEL TERRITORIO HISTÓRICO DE GIPUZKOA",
    )
    return text


@register_fixer("pais_vasco", 2009, 3)
def fix_pais_vasco_2009_03(text: str) -> str:
    text = text.replace("00.– ALFREDO PARTE GUTIÉRREZ", "10.– ALFREDO PARTE GUTIÉRREZ")
    text = _fix_substitutes_declaration(text)
    # Facilitate parsing
    text = text.replace(
        "GIPUZKOAKO KONDAIRA-LURRALDEKO JUNTA ELECTORAL DEL TERRITORIO",
        "JUNTA ELECTORAL DEL TERRITORIO HISTÓRICO DE GIPUZKOA",
    )
    text = text.replace("\n(", " (")
    return text


@register_fixer("pais_vasco", 2012, 10)
def fix_pais_vasco_2012_10(text: str) -> str:
    # TODO: err.pdf
    # Fix missing candidacies
    text = text.replace(
        "14.– BIDEZKO MUNDURANTZ",
        "Candidatura núm. 13: RELLENO\nNO PROCLAMADA\n14.– BIDEZKO MUNDURANTZ",
    )
    # Facilitate parsing
    text = text.replace("UNIÓN PROGRESO Y DEMOCRACIA\n", "UNIÓN PROGRESO Y DEMOCRACIA ")
    return text


@register_fixer("pais_vasco", 2016, 9)
def fix_pais_vasco_2016_09(text: str) -> str:
    if "NATALIA ROJO SOLANA" in text:
        start_line = "NATALIA ROJO SOLANA"
        end_line = "09.– ALBERTO ALONSO MARTÍN"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "REBECA MARTÍN MIGUEL" in text:
        start_line = "10.– REBECA MARTÍN MIGUEL"
        end_line = "24.– ARANTZA RUIZ HUIDOBRO"
        text = fill_missing_numbers(text, start_line, end_line, start_number=11)
    text = text.replace("4.– PARTIDO POPULAR", "Candidatura núm. 4: PARTIDO POPULAR")
    text = text.replace(
        "6.– ESCAÑOS EN BLANCO / AULKI ZURIAK",
        "Candidatura núm. 6: ESCAÑOS EN BLANCO / AULKI ZURIAK",
    )
    text = text.replace(
        "6.– EUSKAL KOMUNISTAK – PARTIDO COMUNISTA DE LOS PUEBLOS DE ESPAÑA",
        "Candidatura núm. 6: EUSKAL KOMUNISTAK – PARTIDO COMUNISTA DE LOS PUEBLOS DE ESPAÑA",
    )
    text = text.replace(
        "6.– CIUDADANOS (C’s)",
        "Candidatura núm. 6: CIUDADANOS (C’s)",
    )
    text = text.replace(
        "4.– PARTIDO SOCIALISTA DE EUSKADI - EUSKADIKO EZKERRA (PSOE)",
        "Candidatura núm. 4: PARTIDO SOCIALISTA DE EUSKADI - EUSKADIKO EZKERRA (PSOE)",
    )
    return text
