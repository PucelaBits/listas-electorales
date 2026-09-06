import re

from ._common import (
    clean_ocr_text,
    fill_missing_numbers,
    fix_nine_line_ocr,
    fix_ten_line_ocr,
    register_fixer,
    remove_single_letter_lines,
)

_ANDALUCIA_MISSING_DOT_RE = r"(\d+)(?=\ [A-ZÁÉÍÓÚÑÜ][A-ZÁÉÍÓÚÑÜa-záéíóúñü\.\-ªº]*\s)"


@register_fixer("andalucia", 1982, 5)
def fix_andalucia_1982_05(text: str) -> str:
    text = text.replace("\nNUM. 10\n27 de Abril de 1982", "")
    text = text.replace("NUM. 10 Página núm. 161", "")
    text = text.replace("NUM. 10 Página núm. 165", "")
    text = text.replace("NUM. 10 27 de Abril de 1982\n", "")
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
    text = re.sub(_ANDALUCIA_MISSING_DOT_RE, r"\1.", text)
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
    text = text.replace("D Francisca Olias Ferrera.\n18", "18. Francisca Olias Ferrera.")
    text = text.replace("MOVIMIENTO COMUNISTA\nN 12.-", "12. MOVIMIENTO COMUNISTA%0\n")
    text = text.replace(
        "- FEDERACION DE ALIANZA POPULAR", "2. FEDERACION DE ALIANZA POPULAR"
    )
    text = text.replace(
        "FEDERACION DE ALIANZA POPULAR.\nN27", "7. FEDERACION DE ALIANZA POPULAR\n"
    )
    text = text.replace(
        "N 1.2. FEDERACION DE ALIANZA POPULAR.", "1. FEDERACION DE ALIANZA POPULAR."
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
    text = text.replace("M2. ", "María ")
    text = text.replace("M2 ", "María ")
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
    text = text.replace("José Rodríguez de la Borbolla\n", "José Rodríguez de la Borbolla ")
    text = text.replace("Salvador lgnacio Bustamante\n", "Salvador Ignacio Bustamante ")
    text = fix_ten_line_ocr(text)
    text = fix_nine_line_ocr(text)
    if "D. Angel Gómez Fuentes." in text:
        start_line = "D. Angel Gómez Fuentes."
        end_line = "D. Fernando Carrasco Miras."
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Alfonso Perales Pizarro" in text:
        start_line = "Alfonso Perales Pizarro."
        end_line = "Serafín Núñez Sánchez."
        text = fill_missing_numbers(text, start_line, end_line, start_number=2)
    elif "José María Fontiberio Carrasco" in text:
        start_line = "José María Fontiberio Carrasco."
        end_line = "José Ruiz Betanzos."
        text = fill_missing_numbers(text, start_line, end_line, start_number=2)
    elif "Manuel Pino Cruz." in text:
        start_line = "Manuel Pino Cruz."
        end_line = "José María Oteros Moros."
        text = fill_missing_numbers(text, start_line, end_line, start_number=3)
        # Manually fix missing "SUPLENTES"
        text = text.replace("\n13. ", "\nSUPLENTES\n13. ")
    elif "Luis Bugella Gómez." in text:
        start_line = "Luis Bugella Gómez."
        end_line = "José Angel Castro Molina."
        text = fill_missing_numbers(text, start_line, end_line, start_number=3)
        start_line = "D. José Sánchez Paba."
        end_line = "D. Juan Santaella Porras."
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Juan Pérez Ramón" in text:
        # Manually fix missing "SUPLENTES"
        text = text.replace("\n14. ", "\nSUPLENTES\n14. ")
        start_line = "Francisco Bustamante Morales (Indep.)"
        end_line = "D2 María Manuela Lorite Rascón (Indep.)"
        text = fill_missing_numbers(text, start_line, end_line, start_number=2)
    elif "Rosa M López López" in text:
        start_line = "D Rosa M López López"
        end_line = "D. Ramón Soler de la Fuente"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
        text = text.replace(
            "N 2.- UNION DE CENTRO DEMOCRATICO\n", "2. UNION DE CENTRO DEMOCRATICO%2\n"
        )
    elif "D. ManuelAnguita Peragon." in text:
        start_line = "D. ManuelAnguita Peragon."
        end_line = "D. Carlos Exposito Lozano."
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Miguel Lendinez Lendinez" in text:
        start_line = "Miguel Lendinez Lendinez"
        end_line = "Juan Catena Viedma"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
        start_line = "Carlos Borja Herrera"
        end_line = "D. Germán Rodríguez Hesles"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Joaquín Jiménez Hidalgo." in text:
        start_line = "Joaquín Jiménez Hidalgo."
        end_line = "Francisco García Jaén."
        text = fill_missing_numbers(text, start_line, end_line, start_number=2)
        start_line = "D Nuria Gutiérrez de Madariaga."
        end_line = "Antonio Domínguez Ballester."
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "Rafael Durán Gónzalez" in text:
        # Manually fix missing "SUPLENTES"
        text = text.replace("\n16. ", "\nSUPLENTES\n16. ")
        text = text.replace(
            "N 5.- UNIFICACION COMUNISTA DE ESPAÑA\n",
            "5. UNIFICACION COMUNISTA DE ESPAÑA%1\n",
        )
        text = text.replace(
            "N 6.- PARTIDO SOCIALISTA DE ANDALUCIA\n",
            "6. PARTIDO SOCIALISTA DE ANDALUCIA%3\n",
        )
        text = text.replace(
            "N 9.- MOVIMIENTO FALANGISTA DE ESPAÑA\n",
            "9. MOVIMIENTO FALANGISTA DE ESPAÑA%0\n",
        )
        text = text.replace("N 10.- MOVIMIENTO COMUNISTA DE\n", "10. MOVIMIENTO COMUNISTA DE%3\n")
        text = text.replace("N2 11.- FALANGE ESPAÑOLA DE LAS J.O.N.S.\n", "11. FALANGE ESPAÑOLA DE LAS J.O.N.S.%0\n")
        text = text.replace("\nN 12.- PARTIDO COMUNISTA De ESPAÑA", "\n12. PARTIDO COMUNISTA De ESPAÑA%1\n")
    elif "Manuel Góngora Canela." in text:
        start_line = "Manuel Góngora Canela."
        end_line = "Rafael Bernal Villa."
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
        text = text.replace("N2 4.- PARTIDO COMUNISTA OBRERO\n", "4. PARTIDO COMUNISTA OBRERO%1\n")
    elif "Leonarda Espada Rodríguez" in text:
        text = text.replace("N 5.- UNIFICACION COMUNISTA DE ESPAÑA\n", "5. UNIFICACION COMUNISTA DE ESPAÑA%2\n")
        text = text.replace("Núm 6. PARTIDO SOCIALISTA DE ANDALUCIA-\n", "6. PARTIDO SOCIALISTA DE ANDALUCIA-%4\n")
        text = text.replace("Núm 7. PARTIDO SOCIALISTA OBRERO\n", "7. PARTIDO SOCIALISTA OBRERO%3\n")
        text = text.replace("Núm 8. PARTIDO COMUNISTA DE ANDALUCIA-\n", "8. PARTIDO COMUNISTA DE ANDALUCIA-%1\n")
        text = text.replace("Núm 9. FUERZA NUEVA\n", "9. FUERZA NUEVA%2\n")
        start_line = "D. Juan José Gil Arauz"
        end_line = "D. José Luna Martínez"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    elif "D María del Carmen García Martín" in text:
        start_line = "D María del Carmen García Martín."
        end_line = "D José Ramón García Bernal."
        text = fill_missing_numbers(text, start_line, end_line, start_number=5)
        text = text.replace("N2 11.- PARTIDO SOCIALISTA\n", "11. PARTIDO SOCIALISTA%2\n")
        text = text.replace("N 13.- PARTIDO COMUNISTA DE ESPAÑA\n", "13. PARTIDO COMUNISTA DE ESPAÑA%4\n")
        text = text.replace("N 14.- MOVIMIENTO FALANGISTA\n", "14. MOVIMIENTO FALANGISTA%0\n")
    # Fix substitutes
    text = text.replace(
        "Aragón.\nN 2.- UNION DE CENTRO DEMOCRATICO\n",
        "Aragón.\n2. UNION DE CENTRO DEMOCRATICO%1\n",
    )
    text = text.replace(
        "Núm 3. . PARTIDO SOCIALISTA DE LOS\n", "Núm 3. PARTIDO SOCIALISTA DE LOS%2\n"
    )
    text = text.replace(
        "5.- PARTIDO SOCIALISTA OBRERO\n", "5.- PARTIDO SOCIALISTA OBRERO%5\n"
    )
    text = text.replace(
        "FEDERACION DE ALIANZA POPULAR.\nN6", "6. FEDERACION DE ALIANZA POPULAR%3"
    )
    text = text.replace(
        "N2 11.- MOVIMIENTO COMUNISTA\nDE ANDALUCIA.\n1. D. Rafael Jesús Lara Batlleria",
        "11. MOVIMIENTO COMUNISTA DE ANDALUCIA%3\n1. D. Rafael Jesús Lara Batlleria",
    )
    text = text.replace("7. UNIFICACION COMUNISTA\n", "7. UNIFICACION COMUNISTA%2\n")
    text = text.replace("9.- FUERZA NUEVA.\n", "9.- FUERZA NUEVA%3\n")
    text = text.replace(
        "10.- MOVIMIENTO FALANGISTA DE ESPAÑA\n",
        "10.- MOVIMIENTO FALANGISTA DE ESPAÑA%0\n",
    )
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
        "PARTIDO SOCIALISTA OBRERO ESPAÑOL-\nN 2.-",
        "2. PARTIDO SOCIALISTA OBRERO ESPAÑOL%3\n",
    )
    text = text.replace(
        "N 3.- UNION DE CENTRO DEMOCRÁTICO\n", "3. UNION DE CENTRO DEMOCRÁTICO%5\n"
    )
    text = text.replace(
        "4. PARTIDO SOCIALITA DE ANDALUCIA-\n", "4. PARTIDO SOCIALITA DE ANDALUCIA %3\n"
    )
    text = text.replace(
        "Ne 7.- PARTIDO SOCIALISTA DE LOS\n", "7. PARTIDO SOCIALISTA DE LOS%2\n"
    )
    text = text.replace(
        "Núm 8. PARTIDO COMUNISTA DE ESPAÑA\n", "8. PARTIDO COMUNISTA DE ESPAÑA%1\n"
    )
    text = text.replace("N 9.- MOVIMIENTO COMUNISTA\n", "9. MOVIMIENTO COMUNISTA%3\n")
    text = text.replace(
        "N2 11.- FALANGE ESPAÑOLA DE LAS JONS.\n",
        "11. FALANGE ESPAÑOLA DE LAS JONS.%5\n",
    )
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
        "Núm 2. FEDERACION DE PARTIDOS DE\n", "2. FEDERACION DE PARTIDOS DE%2\n"
    )
    text = text.replace(
        "N 3.- UNION DE CENTRO DEMOCRATICO\n", "3. UNION DE CENTRO DEMOCRATICO%3\n"
    )
    text = text.replace(
        "N 5.- PARTIDO COMUNISTA DE ANDALUCIA\n",
        "5. PARTIDO COMUNISTA DE ANDALUCIA%4\n",
    )
    text = text.replace(
        "N 6.- PARTIDO SOCIALISTA DE ANDALUCIA-\n",
        "6. PARTIDO SOCIALISTA DE ANDALUCIA-%3\n",
    )
    text = text.replace(
        "N 7.- UNIFICACIÓN COMUNISTA DE ESPAÑA\n",
        "7. UNIFICACIÓN COMUNISTA DE ESPAÑA%4\n",
    )
    text = text.replace(
        "Núm 8. FALANGE ESPAÑOLA DE LA JONS\n", "8. FALANGE ESPAÑOLA DE LA JONS%5\n"
    )
    text = text.replace(
        "N 9.- MOVIMIENTO FALANGISTA DE ESPAÑA\n",
        "9. MOVIMIENTO FALANGISTA DE ESPAÑA%1\n",
    )
    text = text.replace(
        "N 10.- LIGA COMUNISTA REVOLUCIONARIA\n",
        "10. LIGA COMUNISTA REVOLUCIONARIA%0\n",
    )
    text = text.replace(
        "N2 11.- MOVIMIENTO COMUNISTA\n", "N2 11.- MOVIMIENTO COMUNISTA%1\n"
    )
    text = text.replace("N2 12. FUERZA NUEVA\n", "N2 12. FUERZA NUEVA%3\n")
    text = text.replace(
        "11. D Rafael Carrasco Aguera", "11. D Rafael Carrasco Aguera\nSUPLENTES"
    )
    text = text.replace(
        "11. Manuel Peñate Nuñez PCA-PCE.",
        "11. Manuel Peñate Nuñez PCA-PCE.\nSUPLENTES",
    )
    text = text.replace(
        "Núm 5. PARTIDO COMUNISTA DE ANDALUCIA\n",
        "Núm 5. PARTIDO COMUNISTA DE ANDALUCIA%5\n",
    )
    text = text.replace("N 6.- PARTIDO SOCIALISTA.\n", "6. PARTIDO SOCIALISTA.%2\n")
    text = text.replace(
        "11. Manuel Gómez Dominguez.", "11. Manuel Gómez Dominguez.\nSUPLENTES"
    )
    text = text.replace(
        "Núm 8. ASOCIACION POLITICA FUERZA\n", "8. ASOCIACION POLITICA FUERZA%0\n"
    )
    text = text.replace(
        "Núm 9. - PARTIDO SOCIALISTA OBRERO\n", "9. PARTIDO SOCIALISTA OBRERO%5\n"
    )
    text = text.replace("N2 3.- ALIANZA POPULAR\n", "N2 3.- ALIANZA POPULAR%0\n")
    text = text.replace(
        "N 4.- PARTIDO SOCIALISTA DE ANDALUCIA\n",
        "4. PARTIDO SOCIALISTA DE ANDALUCIA%2\n",
    )
    text = text.replace(
        "N 6.- MOVIMIENTO FALANGISTA DE ESPAÑA\n",
        "6. MOVIMIENTO FALANGISTA DE ESPAÑA%0\n",
    )
    text = text.replace(
        "Núm 7. PARTIDO SOCIALISTA OBRERO\n", "7. PARTIDO SOCIALISTA OBRERO%2\n"
    )
    text = text.replace(
        "N 8. SOLIDARIDAD POPULAR ANDALUZA\n", "8. SOLIDARIDAD POPULAR ANDALUZA%1\n"
    )
    text = text.replace("N 10.- ASOCIACION POLITICA\n", "10. ASOCIACION POLITICA%2\n")
    text = text.replace("16. Manuel Durán López.", "SUPLENTES\n16. Manuel Durán López.")
    text = text.replace(
        "Núm 2. ORGANIZACIÓN COMUNISTA DE\n", "2. ORGANIZACIÓN COMUNISTA DE%0\n"
    )
    text = text.replace("N2 3.- FUERZA NUEVA\n", "N2 3.- FUERZA NUEVA%1\n")
    text = text.replace(
        "16. Eduardo Alonso García.", "SUPLENTES\n16. Eduardo Alonso García."
    )
    text = text.replace(
        "N 4.- PARTIDO COMUNISTA DE ANDALUCIA\n",
        "4. PARTIDO COMUNISTA DE ANDALUCIA%2\n",
    )
    text = text.replace("16. Salvador Antonio García Guerra.", "SUPLENTES\n16. Salvador Antonio García Guerra.")
    text = text.replace("N 13.- PARTIDO COMUNISTA OBRERO\n", "13. PARTIDO COMUNISTA OBRERO%0\n")
    text = text.replace("NO FEDERACION DE ALIANZA POPULAR", "3. FEDERACION DE ALIANZA POPULAR%0")
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
    text = re.sub(_ANDALUCIA_MISSING_DOT_RE, r"\1.", text)
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
    text = text.replace("H M9. ", "1. María ")
    text = text.replace("M9. ", "María ")
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
    text = remove_single_letter_lines(text)
    # Fix substitutes
    text = text.replace(
        "2.- CENTRO DEMOCRÁTICO Y SOCIAL (cD.S)",
        "2.- CENTRO DEMOCRÁTICO Y SOCIAL (C.D.S)%1",
    )
    text = text.replace(
        "3.- PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA\n(P.S.O.E DE ANDALUCIA)\n1. José Miguel Salinas Moya",
        "3.- PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA%3\n(P.S.O.E DE ANDALUCIA)\n1. José Miguel Salinas Moya",
    )
    text = text.replace(
        "4.. CENTRO DEMOCRÁTICO Y SOCIAL (C.D.S.)",
        "4.- CENTRO DEMOCRÁTICO Y SOCIAL (C.D.S.)%2",
    )
    text = text.replace("5. PARTIDO HUMANISTA A", "5. PARTIDO HUMANISTA%3")
    text = text.replace(
        "6.- PARTIDO REFORMISTA DEMOCRATICO (P.R.D.)\n1. José Carlos Aguilera Escobar",
        "6.- PARTIDO REFORMISTA DEMOCRATICO (P.R.D.)%2\n1. José Carlos Aguilera Escobar",
    )
    text = text.replace(
        "t 7.- PARTIDO SOCIALISTA DEL PUEBLO ANDALUZ (P.S.P.A.)",
        "7.- PARTIDO SOCIALISTA DEL PUEBLO ANDALUZ (P.S.P.A.)%3",
    )
    text = text.replace(
        "8.- PARTIDO ANDALUCISTA\n1. Salvador Pérez Bueno",
        "8.- PARTIDO ANDALUCISTA%2\n1. Salvador Pérez Bueno",
    )
    text = text.replace(
        "9.- LIBERACION ANDALUZA\n1. Antonio Luis Calderón Díaz",
        "9.- LIBERACION ANDALUZA%3\n1. Antonio Luis Calderón Díaz",
    )
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
    # Fix substitutes
    text = text.replace(
        "16. COALICION ALIANZA POR LA REPUBLICA",
        "16. COALICION ALIANZA POR LA REPUBLICA%1",
    )
    text = text.replace(
        "N 15. PARTIDO COMUNISTA DE ESPAÑA\n(MARXISTA-LENINISTA) P.C. (M-L)\n1. José M Castellano Romero",
        "15. PARTIDO COMUNISTA DE ESPAÑA (MARXISTA-LENINISTA) P.C. (M-L)%2\n1. José M Castellano Romero",
    )
    text = text.replace(
        "16. CENTRO DEMOCRATICO Y SOCIAL", "16. CENTRO DEMOCRATICO Y SOCIAL%3"
    )
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
    # Fix substitute counts
    text = text.replace(
        "Núm. 8. CÓALICION ELECTORAL «FORO Y C.D.S.» (FORO Y C.D.S.)",
        "Núm. 8. COALICIÓN ELECTORAL «FORO Y C.D.S.» (FORO Y C.D.S.)%1",
    )
    text = text.replace(
        "Núm. 4. PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA\n               (PSOE DE ANDALUCIA)\n\n       Núm. 1. Don Gaspar Carlos Zarrías Arévalo.",
        "Núm. 4. PARTIDO SOCIALISTA OBRERO ESPAÑOL DE ANDALUCIA%5\n(PSOE DE ANDALUCIA)\nNúm. 1. Don Gaspar Carlos Zarrías Arévalo.",
    )
    text = text.replace(
        "Núm. 5. FALANGE ESPAÑOLA DE LAS J.O.N.S. (F.E. de las J.O.N.S.)",
        "Núm. 5. FALANGE ESPAÑOLA DE LAS J.O.N.S. (F.E. de las J.O.N.S.)%3",
    )
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
    # Fix substitute counts
    text = text.replace("8.  NACION ANDALUZA (NA)", "8.  NACION ANDALUZA (NA)%2")
    text = text.replace(
        "9.  IZQUIERDA UNIDA LOS VERDES-CONVOCATORIA POR ANDALUCIA (IULV-CA)",
        "9.  IZQUIERDA UNIDA LOS VERDES-CONVOCATORIA POR ANDALUCIA (IULV-CA)%3",
    )
    return text


@register_fixer("andalucia", 2004, 3)
def fix_andalucia_2004_03(text: str) -> str:
    if "CONSEJERIA DE TURISMO Y DEPORTE" in text:
        # Remove preamble
        return ""
    # Fix substitute counts
    text = text.replace(
        "6.  FALANGE ESPAÑOLA DE LAS J.O.N.S. (F.E. DE LAS J.O.N.S.)",
        "6.  FALANGE ESPAÑOLA DE LAS J.O.N.S. (F.E. DE LAS J.O.N.S.)%4",
    )
    text = text.replace(
        "7.  ASAMBLEA DE ANDALUCIA (A)",
        "7.  ASAMBLEA DE ANDALUCIA (A)%3",
    )
    text = text.replace(
        "10.  FALANGE ESPAÑOLA DE LAS JONS (FE-JONS)",
        "10.  FALANGE ESPAÑOLA DE LAS JONS (FE-JONS)%2",
    )
    text = text.replace("11.  UNION NACIONAL (UN)", "11.  UNION NACIONAL (UN)%3")
    return text


@register_fixer("andalucia", 2008, 3)
def fix_andalucia_2008_03(text: str) -> str:
    if "CONSEJERÍA DE AGRICULTURA Y PESCA" in text:
        # Remove preamble
        return ""
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
