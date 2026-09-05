import re

from ._common import (
    clean_ocr_text,
    fill_missing_numbers,
    fix_nine_line_ocr,
    fix_ten_line_ocr,
    register_fixer,
)

_ANDALUCIA_1986_06_MISSING_DOT_RE = r"(\d+)(?=\ [A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜa-záéíóúñü-]+\s)"


def _fix_missing_eleven(text: str) -> str:
    # (?m)    : Multiline mode, so '^' matches the beginning of each line.
    # ^\s*    : Matches the start of the line and any optional leading spaces.
    # (^\s*10\..*\n\s*) : GROUP 1 - Matches the entire "10." line, the newline, and leading spaces of the next line.
    # 1\.     : Matches the "1." that we want to replace.

    pattern = r"(?m)(^\s*10\..*\n\s*)1\."

    # \g<1> inserts everything captured in Group 1, followed by our fixed "11."
    return re.sub(pattern, r"\g<1>11.", text)


@register_fixer("andalucia", 1986, 6)
def fix_andalucia_1986_06(text: str) -> str:
    print(text)
    print(repr(text))
    if "CONSEJERIA DE TURISMO COMERCIO" in text:
        # Remove preamble
        text = (
            "JUNTA ELECTORAL PROVINCIAL DE ALMERIA"
            + text.split("JUNTA ELECTORAL PROVINCIAL DE ALMERIA")[1]
        )
    # Remove header
    text = text.replace("BOJA núm. 50", "")
    # Erratas (err_1.pdf)
    text = text.replace("Miguel Cartés Puentes", "Miguel Cartés Fuentes")
    text = text.replace(
        "Carlos-Javier Ordoñe Rodríguez", "Carlos-Javier Ordoño Rodríguez"
    )
    text = text.replace("Rosario Castellanos Corquera", "Rosario Castellanos Corcuera")
    text = text.replace("Elena Ordoñe Rodríguez", "Elena Ordoño Rodríguez")
    text = text.replace("Pablo Iglesias Roal", "Pablo Iglesias Real")
    text = text.replace("Antonio Mateos Torres", "Antonio Mateos Tores")
    text = text.replace(
        "Juan de la Cruz Carlos Almanes Domínguez",
        "Juan de la Cruz Carlos Almansa Domínguez",
    )
    text = text.replace("Hugo-Fermín Rodríguez Chiara", "Hugo-Fermín Rodríguez Ghiara")
    text = text.replace("Suárez Muyer", "Suárez Muyor")
    text = text.replace("Gloria Gago Vázquez (P.p. )", "Gloria Gago Vázquez (F.P.)")
    text = text.replace(
        "Francisco de Faula Prados Ruiz", "Francisco de Paula Prados Ruiz"
    )

    # Erratas (err_2.pdf)
    text = text.replace("Diego Valderas Sosa (P.C.A.)", "Diego Valderas Sosa (PCA-PCE)")
    text = text.replace(
        "José Luis Pavón Cintado (P.C.P.A.)", "José Luis Pavón Cintado (PCPE)"
    )
    text = text.replace(
        "José Quintero García (P.C.A.)", "José Quintero García (PCA-PCE)"
    )
    text = text.replace(
        "José Zamorano Wisnes (Indep.)", "José Zamorano Wisnes (Independ.)"
    )
    text = text.replace("Manuela Boza Feria (P.C.A.)", "Manuela Boza Feria (PCA-PCE)")
    text = text.replace(
        "Vicente Rufino Rivero (Indep.)", "Vicente Rufino Rivero (Independ.)"
    )
    text = text.replace(
        "Cayetano M. Montenegro Márquez (P.C.P.A.)",
        "Cayetano M. Montenegro Márquez (PCPE)",
    )
    text = text.replace("Enrique Castaño González", "Enrique Costaño González")
    text = text.replace(
        "Rafael Aljama Alcántara (Indep.)", "Rafael Aljama Alcántara (Independ.)"
    )
    text = text.replace(
        "Manuel Tellada Garrido (P.C.P.A.)", "Manuel Tellado Garrido (PCPE)"
    )
    text = text.replace(
        "Mario A. Lobo Romero (P.C.A.)", "Mario A. Lobo Romero (PCA-PCE)"
    )
    text = text.replace(
        "Francisco Vázquez Mojarro (Indep.)", "Francisco Vázquez Mojarro (Independ.)"
    )
    text = text.replace(
        "Juan J. López Cerezo (P.C.A.)", "Juan J. López Cerezo (PCA-PCE)"
    )
    text = text.replace(
        "Diego Rodríguez del Valle (P.C.A.)", "Diego Rodríguez del Valle (PCA-PCE)"
    )
    text = text.replace("Nieves Salinas Alejandra", "Nieves Salinas Alejandre")
    # Duplicate missing substitutes
    text = text.replace(
        "). Dovid González Aguilera",
        "1. David González Aguilera\n2. David González Aguilera\n3. David González Aguilera",
    )
    text = text.replace(
        "2. Juan Jesús Merino Gutiérrez",
        "2. Juan Jesús Merino Gutiérrez\n3. Juan Jesús Merino Gutiérrez",
    )
    text = text.replace(
        "2. Serofín Morillo Medina",
        "2. Serofín Morillo Medina\n3. Serofín Morillo Medina",
    )
    text = text.replace(
        "2. Milagros León Bailén", "2. Milagros León Bailén\n3. Milagros León Bailén"
    )
    # Manuallt fix OCR
    text = text.replace(
        "I.- PARTIDO REFORMISTA DEMOCRATICO (P.R.D.",
        "1. PARTIDO REFORMISTA DEMOCRATICO (P.R.D.)",
    )
    text = text.replace("S- PARTIDO ANDALUCISTA", "5. PARTIDO ANDALUCISTA")
    text = text.replace(
        "JUAN ELECTORAL PROVINCIAL DE HUELVA", "JUNTA ELECTORAL PROVINCIAL DE HUELVA"
    )
    text = text.replace("l PARTIDO ", "1. PARTIDO ")
    text = text.replace(
        "JUNTA ELECTORAL PROVINCIAL DE CADIZ\nCENTRO DEMOCRATICO Y SOCIAL (C.D.S.)",
        "JUNTA ELECTORAL PROVINCIAL DE CADIZ\n1. CENTRO DEMOCRATICO Y SOCIAL (C.D.S.)",
    )
    text = re.sub(_ANDALUCIA_1986_06_MISSING_DOT_RE, r"\1.", text)
    text = text.replace("nO. ", "10. ")
    text = text.replace("vo. ", "10. ")
    text = text.replace("TO ", "10. ")
    text = text.replace("yO. ", "10. ")
    text = text.replace("m1. ", "11. ")
    text = text.replace("IT. ", "11. ")
    text = text.replace("tl.", "11.")
    text = text.replace("nm. ", "11. ")
    text = text.replace("n. ", "11. ")
    text = text.replace("mM. ", "11. ")
    text = text.replace("Mn ", "11. ")
    text = text.replace("mn ", "11. ")
    text = text.replace("m11. ", "11. ")
    text = text.replace("M11. ", "11. ")
    text = text.replace("m3. ", "13. ")
    text = text.replace("Y. ", "1. ")
    text = text.replace("T. ", "1. ")
    text = text.replace("l. ", "1. ")
    text = text.replace("l.. ", "1. ")
    text = text.replace("lt. ", "1. ")
    text = text.replace("). ", "1. ")
    text = text.replace("H M9. ", "1. ")
    text = text.replace("ó Jorge Luis", "6. Jorge Luis")
    text = text.replace("M1. ", "María ")
    text = text.replace(
        "MA Francisco Medina Fernández", "11. Francisco Medina Fernández"
    )
    text = text.replace("EuladioF. Martín Cano", "Euladio F. Martín Cano")
    text = text.replace(". Antonio García Terrada", "1. Antonio García Terrada")
    text = text.replace("ó Francisco Mellado Parra", "6. Francisco Mellado Parra")
    text = text.replace("o Enrique Cortes Sánchez", "Enrique Cortes Sánchez")
    text = text.replace("NA José lópez Benítez", "11. José López Benítez")
    text = text.replace("n Monuel Pérez García", "11. Manuel Pérez García")
    text = text.replace(
        "n Francisca García Caballero", "11. Francisca García Caballero"
    )
    text = text.replace(
        ". Antonio Sánchez Villaverde", "11. Antonio Sánchez Villaverde"
    )
    text = text.replace("17. Gabriel Relaño Canales", "11. Gabriel Relaño Canales")
    text = text.replace("12. Antonio Ruano León", "17. Antonio Ruano León")
    text = text.replace(
        "1. Enrique Sánchez Díaz (P.C.A.-P.C.El",
        "17. Enrique Sánchez Díaz (P.C.A.-P.C.E.)",
    )
    text = text.replace(
        "1. María del Carmen Jiménez Jiménez", "María del Carmen Jiménez Jiménez"
    )
    text = text.replace(
        "10 MS. de los Angeles Corral Casores",
        "10. María de los Angeles Corral Casores",
    )
    text = text.replace(
        "v Monuel Archilla Sánchez (A.P", "11. Manuel Archilla Sánchez (A.P.)"
    )
    text = text.replace(
        "Vicente José Luis E. Aguilar Fernández-Capel Gollart (A.P.) Baños (e.D.p. )",
        "José Luis Aguilar Gollart\nVicente E. Fernández-Capel Baños (P.D.P.)",
    )
    text = text.replace(
        "José Manuel Gard íta Ragel\nLópez Ñ\nFrancisco López",
        "José Manuel García Ragel\nFrancisco López López",
    )
    text = text.replace(
        "Concepción Carmen Jiménez Gómez Siles García de solo",
        "Carmen Jiménez Siles\nConcepción Gómez García de Sola",
    )
    text = text.replace(
        "Gregorio Cano Rodríguez\nv\nRicardo Mateo de Maya 1",
        "Gregorio Cano Rodríguez\nRicardo Mateo de Maya",
    )
    text = text.replace(
        "Alfredo Jesús Antonia Merchán Fernández Jiménez Olmedd",
        "Alfredo Merchán Jiménez\nJesús Antonio Fernández Olmedo",
    )
    text = text.replace("Antonio 1. Diaz Rodríguez", "Antonio L. Díaz Rodríguez")
    text = _fix_missing_eleven(text)
    text = fix_ten_line_ocr(text)
    text = fix_nine_line_ocr(text)
    if "Domingo Domenech Cruz" in text:
        start_line = "Domingo Domenech Cruz"
        end_line = "Francisca Crespo lópez"
        text = fill_missing_numbers(text, start_line, end_line, start_number=5)
    elif "José Guerrero Casaus" in text:
        start_line = "José Guerrero Casaus"
        end_line = "Juan Carlos Murga Tejada"
        text = fill_missing_numbers(text, start_line, end_line, start_number=3)
        start_line = "Manuel Llamas Sanjuan"
        end_line = "Antonio Luque Prados"
        text = fill_missing_numbers(text, start_line, end_line, start_number=4)
    elif "Antonio José Peláez Montalvo" in text:
        start_line = "Antonio José Peláez Montalvo"
        end_line = "Daniel Torres Castillo"
        text = fill_missing_numbers(text, start_line, end_line, start_number=5)
    elif "Jasé Carlos Espin Ballesta" in text:
        start_line = "Jasé Carlos Espin Ballesta"
        end_line = "José Ruiz Higueras"
        text = fill_missing_numbers(text, start_line, end_line, start_number=4)
    elif "Francisco Palomo Aragón" in text:
        start_line = "Francisco Palomo Aragón"
        end_line = "Juan José Caballero Montilla"
        text = fill_missing_numbers(text, start_line, end_line, start_number=3)
    elif "Elisa García Delgado" in text:
        start_line = "Elisa García Delgado"
        end_line = "Diego Honorio Moreno Muñoz"
        text = fill_missing_numbers(text, start_line, end_line, start_number=4)
    elif "Enrique linde Cirujano" in text:
        start_line = "Enrique linde Cirujano"
        end_line = "Francisco Parra Medina"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Antonio Luis Calderón Díaz" in text:
        start_line = "Antonio Luis Calderón Díaz"
        end_line = "Euladio F. Martín Cano"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Mariano Barrios Moga" in text:
        start_line = "Mariano Barrios Moga"
        end_line = "Francisco López López"
        text = fill_missing_numbers(text, start_line, end_line, start_number=11)
    text = text.replace("Dovid", "David")
    text = text.replace("Monuel", "Manuel")
    return text


_ANDALUCIA_1990_06_D_RE = re.compile(r"-?(\d+)\.?\s*D[a-zA-Zªº\-']?\.?\.? ")


@register_fixer("andalucia", 1990, 6)
def fix_andalucia_1990_06(text: str) -> str:
    # Remove footer
    if "PLAZOS DE SUSCRIPCION" in text:
        return ""
    # Remove header
    text = text.replace("BOJA núm. 43", "")
    # Erratas (err.pdf)
    text = text.replace("N 2. VERDES DE ANDALUCIA (V.A.)", "N 2. VERDES DE ANDALUCIA")
    text = text.replace(
        "Bruno Juan Carrera Cortés de Maia", "Bruno Juan Carrera Cortez de María"
    )
    text = text.replace("Jesús Romera Domené", "Jesús Romera Domene")
    text = text.replace(
        "M Angeles Cervantes Beneyto", "María de los Angeles Cervantes Beneyto"
    )
    text = text.replace("José María Gómez Terreros", "José María Gómez Terrero")
    text = text.replace("Luisa Ibáñez Cuadrado", "Luisa Ybáñez Cuadrado")
    text = text.replace(
        "N 4. IZQUIERDA UNIDA-CONVOCATORIA POR\nANDALUCIA (1.U.-C.A.)",
        "N 4. IZQUIERDA UNIDA-CONVOCATORIA POR ANDALUCIA (IU-CA)",
    )
    text = text.replace(
        "María Mercedes Salguero Borrero", "María de las Mercedes Salguero Borrero"
    )
    text = text.replace(
        "5 6 D. D. Juan Ildefonso Antonio Guerrero Díaz Romero Seijó",
        "5. Idelfonso Guerrero Seijo\n6. Juan Antonio Guerrero Díaz Romero",
    )
    text = text.replace("María Josefa Pineda Ortega", "Joséfa Pineda Ortega")
    text = text.replace("Ricardo Mazachis Rodríguez", "Ricardo Masachís Rodríguez")
    text = text.replace("María Reyes Muñoz Terol", "María de los Reyes Muñoz Terol")
    text = text.replace(
        "Pilar Martín-Peñasco Román", "María del Pilar Martín-Peñasco Román"
    )
    text = text.replace("José Panés Muñoz", "José Panes Muñoz")
    text = text.replace("N 9. PARTIDO ANDALUCISTA (P.A.)", "N 9. PARTIDO ANDALUCISTA")
    text = text.replace("Carmen Lovelle Alen", "María del Carmen Lovelle Alen")
    text = text.replace("María de los Milagros Isla Barba", "María Milagros Isla Barba")
    text = text.replace("P.T.E.-U.C.", "PTE-UC")
    text = text.replace(
        "M Angeles Alvarez Martínez", "María de los Angeles Alvarez Martínez"
    )
    text = text.replace("Salvador Blanco Ruiz'", "Salvador Blanco Rubio")
    text = text.replace("Carmen Mata Varelo", "Carmen Mata Valero")
    text = text.replace(
        "N 11. PARTIDO AGRUPACION RUIZ MATEOS", "N 11. AGRUPACION RUIZ MATEOS"
    )
    text = text.replace("Manuel Macías Romero", "José Manuel Macías Ramero")
    text = text.replace(
        "Fernández-Piñar Afán de Ri-\n\nvera", "Fernández-Piñar Afán de Ribera"
    )
    text = text.replace(
        "N 2. PARTIDO SOCIALISTA OBRERO ESPAÑOL\n\n(P.S.O.E. DE ANDALUCIA)",
        "N 2. PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA (PSOE DE ANDALUCIA)",
    )
    text = text.replace("N 4. PARTIDO ANDALUCISTA (P.A.)", "N 4. PARTIDO ANDALUCISTA")
    text = text.replace("María Victoria Martín Noguez", "María Victoria Martín Nogues")
    text = text.replace("Francisco Domínguez Chaves", "Francisco Domínguez Chavez")
    text = text.replace("Miguel Bernáldez Prada", "Miguel Bernardez Prada")
    text = text.replace("María José Ligero Rey", "María José Lijero Rey")
    text = text.replace("N 13. PARTIDO ANDALUCISTA (P.A.)", "N 13. PARTIDO ANDALUCISTA")
    # Remove candidacy name
    text = text.replace(". PCE (M-1)", "")
    text = text.replace(". PCE (M-L)", "")
    text = text.replace(".\nPCE (M-L)", "")
    text = text.replace(".\nPCE (M-1)", "")
    text = text.replace(". Independiente", "")
    text = text.replace(". Indepen-\ndiente", "")
    text = text.replace(". Indepen-\n\ndiente", "")
    text = text.replace(".\nIndependiente", "")
    text = text.replace("lindependiente)", "")
    text = text.replace("tindependiente)", "")
    text = text.replace("lindependientel", "")
    text = text.replace("lindependien-\n\ntel", "")

    # Duplicate missing substitutes
    text = text.replace(
        "1 D. Juan Carlos Chamón Ibáñez",
        "1. Juan Carlos Chamón Ibáñez\n2. Juan Carlos Chamón Ibáñez\n3. Juan Carlos Chamón Ibáñez",
    )
    text = text.replace(
        "2 D. Jesús Ledro Vargas", "2 D. Jesús Ledro Vargas\n3 D. Jesús Ledro Vargas"
    )
    # Manuallt fix OCR
    text = text.replace("D.'", "D. ")
    text = text.replace("D.-", "D. ")
    text = text.replace(
        "N 3. COALICION IZQUIERDA UNIDA-CONVO-\nCATORIA POR ANDALUCIA 1.U.-C.A",
        "3. COALICION IZQUIERDA UNIDA-CONVOCATORIA POR ANDALUCIA (I.U.-C.A.)",
    )
    text = re.sub(_ANDALUCIA_1990_06_D_RE, r"\1. ", text)
    text = text.replace("HD. Juan", "11. Juan")
    text = text.replace("D. Manuel Virella Redondo", "1. Manuel Virella Redondo")
    text = text.replace("p. Salud de Silva García", "1. Salud de Silva García")
    text = text.replace("D. Juan Duarte Berrocal", "1. Juan Duarte Berrocal")
    text = text.replace("1 Ó D.", "16. ")
    text = text.replace("2D..", "2. ")
    text = text.replace("l D. ", "1. ")
    text = text.replace("9 P. ", "9. ")
    text = text.replace("9 Pp. ", "9. ")
    text = text.replace("(A.R.) l", "(A.R.)")
    text = text.replace("Óó D. ", "6. ")
    text = text.replace("ó Dr.", "6. ")
    text = text.replace("ó D.", "6. ")
    text = text.replace("Ó D.", "6. ")
    text = text.replace("ó D-.", "6. ")
    text = text.replace("ó. ", "6. ")
    text = text.replace("O De.", "10. ")
    text = text.replace("10'D. ", "10. ")
    text = text.replace("1T D. ", "11. ")
    text = text.replace("T0 D. ", "10. ")
    text = text.replace("1O D. ", "10. ")
    text = text.replace("TO D. ", "10. ")
    text = text.replace("T D. ", "1. ")
    text = text.replace("1 pr. ", "1. ")
    text = text.replace("T Dr. ", "1. ")
    text = text.replace("Í Dr. ", "1. ")
    text = text.replace("T' D. ", "1. ")
    text = text.replace("TD. ", "1. ")
    text = text.replace("1 .D.", "1. ")
    text = text.replace("y Dr. ", "1. ")
    text = text.replace("Y D.", "1. ")
    text = text.replace("- SUPLENTES", "SUPLENTES")
    text = text.replace("SLIPLENTES", "SUPLENTES")
    text = text.replace("o SUPLENTES", "SUPLENTES")
    text = clean_ocr_text(text)
    return text


@register_fixer("andalucia", 1994, 6)
def fix_andalucia_1994_06(text: str) -> str:
    if "EXPOSICION DE MOTIVOS" in text:
        # Remove preamble
        return ""
    # Erratas (err.pdf)
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
    text = text.replace(
        "1. Don Mario García Guillén",
        "1. Don Mario García Guillén\n2. Don Mario García Guillén\n3. Don Mario García Guillén",
    )
    text = text.replace(
        "Núm. .- PARTIDO POPULAR (P.P.)", "Núm. 1. PARTIDO POPULAR (P.P.)"
    )
    # Hardcoded fixes for OCR
    text = text.replace("1.-.PARTIDO POPULAR", "1. PARTIDO POPULAR")
    text = text.replace(
        "1'. Don Mariano JuncoGonzález", "1. Don Mariano Junco González"
    )
    text = text.replace(
        "5.- IZQUIERDA UNIDA LOS VERDES-C(INVOCATORIA POR ANDALUCIA",
        "5.- IZQUIERDA UNIDA LOS VERDES-CONVOCATORIA POR ANDALUCIA",
    )
    text = text.replace(
        r"i\lúrn. 5. Don Manuel Jesús González. Gamerá.",
        "Núm. 5. Don Manuel Jesús González Gamero.",
    )
    text = text.replace(
        "Núm. 1-0. Doña María del Mar García Andrés.",
        "Núm. 10. Doña María del Mar García Andrés.",
    )
    text = text.replace(
        "Núm. 2. Doña María de la Paz Llavero del Pozo",
        "Núm. 3. Doña María de la Paz Llavero del Pozo",
    )
    text = text.replace("Don Manuel Rodríguez Gamiz", "5. Don Manuel Rodríguez Gamiz")
    text = text.replace("Don Francilco Lorenzo Cuevas", "Don Francisco Lorenzo Cuevas")
    text = text.replace(
        "5, Don Joaquín Jesús Galán Pérez", "5. Don Joaquín Jesús Galán Pérez"
    )
    text = text.replace(
        "7.? Don Francisco Martín Rodríguez", "7. Don Francisco Martín Rodríguez"
    )
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
    # Erratas (err.pdf)
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
    # Erratas (err.pdf)
    text = text.replace("Matilde Ortiz Arcas", "Matilde Ortiz Arca")
    text = text.replace(
        "Concepción del Carmen Muñoz Sánchez", "Concepción del Carmelo Muñoz Sánchez"
    )
    text = text.replace(
        "Javier Vicente Del Moral Quevedo", "Juan Vicente Del Moral Quevedo"
    )
    text = text.replace("Nazaret Navarro Todelado", "Nazaret Navarro Toledano")
    return text
