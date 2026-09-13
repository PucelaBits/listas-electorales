from ._common import fill_missing_numbers, register_fixer


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
