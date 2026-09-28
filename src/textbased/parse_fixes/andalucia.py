import re

from common import NAME_WHITELIST_CHARS

from ._common import (
    clean_ocr_numbers,
    fix_maria_ocr,
    register_fixer,
    remove_single_letter_lines,
)


@register_fixer("andalucia", 1982, 5)
def fix_andalucia_1982_05(text: str) -> str:
    text = text.replace("NUM. 10 Página núm. 161", "")
    text = text.replace("NUM. 10 Página núm. 165", "")
    text = text.replace("Página núm. 158 B.O.J.A.", "")
    text = text.replace("Página núm.", "")
    text = text.replace("NUM. 10  157", "")
    text = text.replace("en la lista figurando como número 1 Fernando", "")
    # Fix typos
    text = text.replace("13 D Ana María Melero Casado.", "11. Ana María Melero Casado.")
    # Manually fix OCR errors
    text = text.replace(
        "14 José Francisco Olea Castellano Varón. Rodríguez.\n15",
        "14. José Olea Varón\n15. Francisco Castellano Rodríguez.",
    )
    text = remove_single_letter_lines(text)
    text = text.replace("D2.lidefonsa Montalban Duran", "12. Ildefonsa Montalban Duran")
    text = text.replace("Josefa Perales Sedano.\n13", "13. Josefa Perales Sedano.")
    text = text.replace(
        "Dp Monserrat Martínez García.\n13", "13. Monserrat Martínez García."
    )
    text = text.replace(
        "D María de los Angeles Duarte Vázquez\n11",
        "11. María de los Angeles Duarte Vázquez.",
    )
    text = text.replace(
        "D. Bartolome Antero Jimenez Antonio\n14",
        "14. Bartolome Antero Jimenez Antonio.",
    )
    text = text.replace("D.José Ruiz Martín.\n14", "14. José Ruiz Martín.")
    text = text.replace(
        "D Francisca Olias Ferrera.\n18", "18. Francisca Olias Ferrera."
    )
    text = text.replace("MOVIMIENTO COMUNISTA\nN 12.-", "12. MOVIMIENTO COMUNISTA\n")
    text = text.replace(
        "- FEDERACION DE ALIANZA POPULAR", "2. FEDERACION DE ALIANZA POPULAR"
    )
    text = text.replace(
        "FEDERACION DE ALIANZA POPULAR.\nN27", "7. FEDERACION DE ALIANZA POPULAR\n"
    )
    text = text.replace(
        "N 1.2. FEDERACION DE ALIANZA POPULAR.", "1. FEDERACION DE ALIANZA POPULAR."
    )
    text = text.replace(
        "NO FEDERACION DE ALIANZA POPULAR", "3. FEDERACION DE ALIANZA POPULAR"
    )
    text = text.replace(
        "18. José Luis Rios Moreno.\nN2. PARTIDO SOCIALISTA OBRERO",
        "18. José Luis Rios Moreno.\n7. PARTIDO SOCIALISTA OBRERO",
    )
    text = text.replace(
        "FEDERACION DE ALIANZA POPULAR.\nN6", "6. FEDERACION DE ALIANZA POPULAR"
    )
    text = text.replace(
        "PARTIDO SOCIALISTA OBRERO ESPAÑOL-\nN 2.-",
        "2. PARTIDO SOCIALISTA OBRERO ESPAÑOL",
    )
    text = text.replace("D2\n", "")
    text = text.replace("Dp\n", "")
    text = text.replace("N2. ", "Núm 2. ")
    text = text.replace("N3", "Núm 3. ")
    text = text.replace("N4. ", "Núm 4. ")
    text = text.replace("N25. ", "Núm 5. ")
    text = text.replace("N5. ", "Núm 5. ")
    text = text.replace("N6. ", "Núm 6. ")
    text = text.replace("No7. ", "Núm 7. ")
    text = text.replace("N7. ", "Núm 7. ")
    text = text.replace("N27. ", "Núm 7. ")
    text = text.replace("N8. ", "Núm 8. ")
    text = text.replace("N9. ", "Núm 9. ")
    text = text.replace("N9 ", "Núm 9. ")
    text = text.replace("D2. ", ". ")
    text = fix_maria_ocr(text)
    text = text.replace("D2. María Linares Capel.", "María Linares Capel.")
    text = text.replace("11 p Obdulia Vázquez Cabreja", "11. Obdulia Vázquez Cabreja")
    text = text.replace(
        "D M Pilar Rodriíguez Tuset..", "9. María Pilar Rodríguez Tuset."
    )
    text = text.replace("1.4.", "14.")
    text = text.replace("12 pD", "12. ")
    text = text.replace("Su\nplentes", "SUPLENTES")
    text = text.replace(
        "de 10. Juan Francisco Rodríguez Márquez",
        "10. Juan Francisco Rodríguez Márquez",
    )
    text = text.replace(
        "D María Loreto Fernández-Nieto\n", "María Loreto Fernández-Nieto "
    )
    text = text.replace(
        "D María de la Concepción García\n", "María de la Concepción García "
    )
    text = text.replace(
        "D Elena del Carmen Fernández de la\n", "Elena del Carmen Fernández de la "
    )
    text = text.replace(
        "Juan Francisco de Asís Ibañez\n", "Juan Francisco de Asís Ibañez "
    )
    text = text.replace(
        "Inmaculada Concepción Fernández\n", "Inmaculada Concepción Fernández "
    )
    text = text.replace("Gervasio Manuel Hernández\n", "Gervasio Manuel Hernández ")
    text = text.replace(
        "José Antonio Sánchez-Collado\n", "José Antonio Sánchez-Collado "
    )
    text = text.replace(
        "Rafael-Carlos Fernández Piñar Afán\n", "Rafael-Carlos Fernández Piñar Afán "
    )
    text = text.replace(
        "D Emiliano Sanz Escalera (Unión de\n", "Emiliano Sanz Escalera (Unión de "
    )
    text = text.replace(
        "José Luis García Palacios (Unión de\n", "José Luis García Palacios (Unión de "
    )
    text = text.replace(
        "Antonio Jesús Barragan de las\n", "Antonio Jesús Barragan de las "
    )
    text = text.replace(
        "José Antonio Marin Rite. PSOE de\n", "José Antonio Marin Rite. PSOE de "
    )
    text = text.replace(
        "José Rodríguez de la Borbolla\n", "José Rodríguez de la Borbolla "
    )
    text = text.replace("Salvador lgnacio Bustamante\n", "Salvador Ignacio Bustamante ")
    # Fix substitutes
    text = text.replace(
        "12. Antonio Santacruz Fernández.",
        "12. Antonio Santacruz Fernández.\nSUPLENTES",
    )
    text = text.replace(
        "12. Pedro Pozuelo Gómez.", "12. Pedro Pozuelo Gómez.\nSUPLENTES"
    )
    text = text.replace(
        "12. D Miguel Angel Rubio Palomino.",
        "12. Miguel Angel Rubio Palomino.\nSUPLENTES",
    )
    text = text.replace("12. Pedro Moreno Beca.", "12. Pedro Moreno Beca.\nSUPLENTES")
    text = text.replace(
        "13. Juan Salguero Maldonado.", "13. Juan Salguero Maldonado.\nSUPLENTES"
    )
    text = text.replace(
        "13. Pedro María Revilla López.", "13. Pedro María Revilla López.\nSUPLENTES"
    )
    text = text.replace(
        "13. D María Lourdes Ropero García",
        "13. D María Lourdes Ropero García\nSUPLENTES",
    )
    text = text.replace(
        "13. Ignacio Nogueras Rodríguez", "13. Ignacio Nogueras Rodríguez\nSUPLENTES"
    )
    text = text.replace(
        "11. D Rafael Carrasco Aguera", "11. D Rafael Carrasco Aguera\nSUPLENTES"
    )
    text = text.replace(
        "11. Manuel Peñate Nuñez PCA-PCE.",
        "11. Manuel Peñate Nuñez PCA-PCE.\nSUPLENTES",
    )
    text = text.replace(
        "11. Manuel Gómez Dominguez.", "11. Manuel Gómez Dominguez.\nSUPLENTES"
    )
    text = text.replace("16. Manuel Durán López.", "SUPLENTES\n16. Manuel Durán López.")
    text = text.replace(
        "16. Eduardo Alonso García.", "SUPLENTES\n16. Eduardo Alonso García."
    )
    text = text.replace(
        "16. Salvador Antonio García Guerra.",
        "SUPLENTES\n16. Salvador Antonio García Guerra.",
    )
    return text


def _fix_missing_eleven(text: str) -> str:
    # Fixes missing "11." when the previous line is "10." and the next line starts with 1.
    pattern = r"(?m)(^\s*10\..*\n\s*)1\."
    return re.sub(pattern, r"\g<1>11.", text)


@register_fixer("andalucia", 1986, 6)
def fix_andalucia_1986_06(text: str) -> str:
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
    text = text.replace("H M9. ", "1. María ")
    text = text.replace("M9. ", "María ")
    text = text.replace("ó Jorge Luis", "6. Jorge Luis")
    text = fix_maria_ocr(text)
    text = text.replace(
        "MA Francisco Medina Fernández", "11. Francisco Medina Fernández"
    )
    text = text.replace("EuladioF. Martín Cano", "Euladio F. Martín Cano")
    text = text.replace("o Enrique Cortes Sánchez", "Enrique Cortes Sánchez")
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
        "Gregorio Cano Rodríguez\nv\nRicardo Mateo de Maya 1",
        "Gregorio Cano Rodríguez\nRicardo Mateo de Maya",
    )
    text = text.replace("Antonio 1. Diaz Rodríguez", "Antonio L. Díaz Rodríguez")
    text = _fix_missing_eleven(text)
    text = text.replace("Dovid", "David")
    text = text.replace("Monuel", "Manuel")
    text = remove_single_letter_lines(text)
    return text


_ANDALUCIA_1990_06_D_RE = re.compile(r"-?(\d+)\.?\s*D[a-zA-Zªº\-']?\.?\.? ")


@register_fixer("andalucia", 1990, 6)
def fix_andalucia_1990_06(text: str) -> str:
    # Remove preamble
    text = text.replace("1. Disposiciones", "")
    # Remove footer
    if "PLAZOS DE SUSCRIPCION" in text:
        return ""
    # Remove header
    text = text.replace("BOJA núm. 43", "")
    text = text.replace("núm. 43 sSevilla Z8 de mayo de TYYu", "")
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
    # Manuallt fix OCR
    text = text.replace("D.'", "D. ")
    text = text.replace("D.-", "D. ")
    text = text.replace(
        "N 3. COALICION IZQUIERDA UNIDA-CONVO-\nCATORIA POR ANDALUCIA 1.U.-C.A",
        "3. COALICION IZQUIERDA UNIDA-CONVOCATORIA POR ANDALUCIA (I.U.-C.A.)",
    )
    text = text.replace(
        "N 17. COALICIÓN ALIANZA POR LA REPUBLICA",
        "11. COALICIÓN ALIANZA POR LA REPUBLICA",
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
    text = clean_ocr_numbers(text)
    # Fix misnumbered candidacies
    text = text.replace(
        "mí N 8. FRENTE ANDALUZ DE LIBERACION (F.A.L)",
        "7. RELLENO\nNO PROCLAMADA\n8. FRENTE ANDALUZ DE LIBERACION (F.A.L.)",
    )
    text = text.replace(
        "CADIZ\nN 2. PARTIDO SOCIALISTA OBRERO ESPAÑOL\n",
        "CADIZ\n1. RELLENO\nNO PROCLAMADA\n 2. PARTIDO SOCIALISTA OBRERO ESPAÑOL\n",
    )
    text = text.replace(
        "N 2. PARTIDO COMUNISTA DE ESPAÑA",
        "1. RELLENO\nNO PROCLAMADA\n2. PARTIDO COMUNISTA DE ESPAÑA",
    )
    text = text.replace(
        "N 19. PARTIDO FRENTE ANDALUZ",
        "18. RELLENO\nNO PROCLAMADA\n19. PARTIDO FRENTE ANDALUZ",
    )
    text = text.replace("' N 3", "3. ")
    text = re.sub(r"Ne\.? (?=\s*[0-9])", "Candidatura núm.: ", text)
    return text


@register_fixer("andalucia", 1994, 6)
def fix_andalucia_1994_06(text: str) -> str:
    if "EXPOSICION DE MOTIVOS" in text:
        # Remove preamble
        return ""
    # Erratas (err.pdf)
    text = text.replace(
        "PROVINCIA DE*MALAGA\nNúm. 1.- PARTIDO POPULAR (P.P.)",
        "PROVINCIA DE MALAGA \nNúm. 1. PARTIDO POPULAR DE ANDALUCIA (P.P.)",
    )
    text = text.replace("Rafael GraCia Contreras", "Rafael García Contreras")
    text = text.replace("Manuel Ruiz Madruga", "Miguel Ruiz Madruga")
    text = text.replace("Peñuelas Cancharro", "Peñuelas Lancharro")
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
    text = text.replace("1.2. Don José Selma García", "12. Don José Selma García")
    text = text.replace("Núm. J. Don Juan Oleda Sanz", "Núm. 1. Don Juan Oleda Sanz")
    text = text.replace("Suplerites", "Suplentes")
    text = text.replace("Sliplentes", "Suplentes")
    text = text.replace("-Suplentes", "Suplentes")
    text = text.replace("?odríguez", "Rodríguez")
    # Fix the "Núm." OCR errors
    text = re.sub(
        r"[NÑ][" + NAME_WHITELIST_CHARS + r"]{1,5}\.(?=\s*[0-9])", "Núm. ", text
    )
    text = text.replace("Minn:", "Núm.")
    text = text.replace("N6m.", "Núm.")
    text = clean_ocr_numbers(text)
    text = text.replace(" -,", " ")
    text = text.replace("_", " ")
    text = text.replace(
        "PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA\n",
        "PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA ",
    )
    return text


@register_fixer("andalucia", 1996, 3)
def fix_andalucia_1996_03(text: str) -> str:
    if "CONSEJERIA DE TRABAJO Y ASUNTOS SOCIALES" in text:
        # Remove preamble
        return ""
    text = text.replace(
        "4.- PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA\n",
        "4.- PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA ",
    )
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
    return text


@register_fixer("andalucia", 2008, 3)
def fix_andalucia_2008_03(text: str) -> str:
    if "CONSEJERÍA DE AGRICULTURA Y PESCA" in text:
        # Remove preamble
        return ""
    text = text.replace("Orden Nombre y apellidos\n", "")
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


@register_fixer("andalucia", 2012, 3)
def fix_andalucia_2012_03(text: str) -> str:
    # Fix for false positive date
    text = text.replace(
        "PARTIDO DEL MOVIMIENTO CIUDADANO 15 MAYO",
        "PARTIDO DEL MOVIMIENTO CIUDADANO 15-MAYO",
    )
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


@register_fixer("andalucia", 2018, 12)
def fix_andalucia_2018_12(text: str) -> str:
    text = text.replace("�����Ángela Gallego Reina", "Ángela Gallego Reina")
    return text
