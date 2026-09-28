import re

from ._common import (
    LOWER_CANDIDATE_NAME_REGEX,
    NUMBER_MAP,
    UPPER_CANDIDATE_NAME_REGEX,
    clean_ocr_numbers,
    number_candidates,
    register_fixer,
)

_CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER = 1
_CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER_UPPER = 1


@register_fixer("castilla_la_mancha", 1999, 6)
def fix_castilla_la_mancha_1999_06(text: str) -> str:
    # Remove preamble
    if "Don PEDRO SALDAÑA PEÑA" in text:
        text = text.split("Don PEDRO SALDAÑA PEÑA")[-1]
    text = text.replace("en el artículo\n", "en el artículo ")
    text = text.replace("ha acordado\n", "ha acordado ")
    text = text.replace("\nBDICLTO\n", " EDICTO ")
    text = text.replace("CANDIDATURA NÚMERO DOS", "3344\nCANDIDATURA NÚMERO DOS")
    text = text.replace("NÚMERO TRES\nCANDIDATURA", "CANDIDATURA NÚMERO TRES")
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}\n", f"CANDIDATURA NÚM. {number} "
        )
        text = text.replace(
            f"CANDIDATURA NUMERO {number_text}\n", f"CANDIDATURA NÚM. {number} "
        )
    # Fix OCR
    text = text.replace(
        "José Antonio Parra Jiménez.\nN2",
        "José Antonio Parra Jiménez.\n2. Marcelino Picazo Fuentes",
    )
    text = text.replace("2.- rtiida 2 La 0 DICTU panoi-Drogres 'OE", "Candidatura número 2: Partido Socialista Obrero Español-progresistas (PSOE)")
    text = text.replace("3. UJIERDA UNIDA - DE CASTILLA - LA", "Candidatura número 3: IZQUIERDA UNIDA - DE CASTILLA - LA MANCHA (I.U.)")
    text = text.replace("HO NA UNAJ SEA LANU EN", "Candidatura número 4: TIERRA COMUNERA-PARTIDO NACIONALISTA CASTELLANO (TC-PNC)")
    text = text.replace("5.- PARTIDO HUMANISTA (P.H.).-", "Candidatura número 5: PARTIDO HUMANISTA (P.H.)")
    text = text.replace("SANTIAGO CASERO PEINADO", "Candidatura número 6: Falange Española de las JONS (FE-JONS)\nSANTIAGO CASERO PEINADO")
    text = text.replace("EP IE P. -) o -", "Candidatura número 7: PARTIDO DE LOS AUTÓNOMOS DE ESPAÑA Y DE LAS AGRUPACIONES INDEPENDIENTES ESPAÑOLAS (P.A.E.i)")
    text = text.replace("8.- UNION CENTRISTA-CENTRO DEMOCRATICO", "Candidatura número 8: UNION CENTRISTA-CENTRO DEMOCRATICO")
    text = text.replace("9.- PARTIDO REGIONALISTA DE CASTILLA LA MANCHA (PRCM ).-", "Candidatura número 9: PARTIDO REGIONALISTA DE CASTILLA LA MANCHA (PRCM )")
    text = text.replace("10.- PARTIDO DEMOCRATA ESPAÑOL (PADE)", "Candidatura número 10: PARTIDO DEMOCRATA ESPAÑOL (PADE)")
    text = text.replace("2.- TIERRA COMUNERA-PARTIDO NACIONALISTA CASTELLANO", "Candidatura número 2: TIERRA COMUNERA-PARTIDO NACIONALISTA CASTELLANO")
    text = text.replace("3.- PARTIDO POPULAR (P.P.)", "Candidatura número 3: PARTIDO POPULAR (P.P.)")
    text = text.replace("4.- PARTIDO HUMANISTA. (P.H.)", "Candidatura número 4: PARTIDO HUMANISTA (P.H.)")
    text = text.replace("5. RE LISTA DE LLA", "Candidatura número 5: PARTIDO REGIONALISTA DE CASTILLA LA MANCHA (PRCM)")
    text = text.replace("6.- IZQUIERDAUNIDA-ISQUIERPA DE CASTILLA LA MANCHA.", "Candidatura número 6: IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA ")
    text = text.replace("FALANGE ESPAÑOLA DELAS J.O.N.S.\nIFB-7.0.M.85)", "Candidatura número 7: FALANGE ESPAÑOLA DE LAS J.O.N.S. (FE-JONS)")
    text = text.replace("8.- UNION CENTRISTA-( ENTRODEMOCRATICO Y SOCIAL\nJU. -D08-)", "Candidatura número 8: UNION CENTRISTA-CENTRO DEMOCRATICO Y SOCIAL (U.C.C.D.S.)")
    text = text.replace("1-Partido Socialista Obrero Español -progresistas", "Candidatura número 1: Partido Socialista Obrero Español-progresistas (PSOE)")
    text = text.replace("2- IZQUIERDA UNIDA- IZQUIERDA DE CASTILLA-LA\n", "Candidatura número 2: IZQUIERDA UNIDA- IZQUIERDA DE CASTILLA-LA ")
    text = text.replace("3- PARTIDO POPULAR\n", "Candidatura número 3: PARTIDO POPULAR ")
    text = text.replace("4.- PARTIDO momia\n", "Candidatura número 4: PARTIDO HUMANISTA ")
    text = text.replace("5- TIERRA COMUNERA url PARTIDO NACIONALISTA\nCASTELLANO\nTC-PNC", "Candidatura número 5: TIERRA COMUNERA-PARTIDO NACIONALISTA CASTELLANO (TC-PNC)")
    text = text.replace("6 - PARTIDO DE LOS AUTONOMOS DE ESPAÑA Y DE LAS\n", "Candidatura número 6: PARTIDO DE LOS AUTONOMOS DE ESPAÑA Y DE LAS ")
    text = text.replace("7.- PARTIDO REGIONALISTA DE GUADALAJARA (P.R.GU.)", "Candidatura número 7: PARTIDO REGIONALISTA DE GUADALAJARA (P.R.GU.)")
    text = text.replace("98 -UNION CENTRISTA-CENTRO DEMOCRATICO Y SOCIAL\n", "Candidatura número 8: UNION CENTRISTA-CENTRO DEMOCRATICO Y SOCIAL ")
    text = text.replace("9-PARTIDO REGIONALLISTA DE CASTILLA LA NANCHA\n", "Candidatura número 9: PARTIDO REGIONALLISTA DE CASTILLA LA MANCHA ")
    text = text.replace("10- FALANGE ESPAÑOLA DE LAS J.0.N.8.", "Candidatura número 10: FALANGE ESPAÑOLA DE LAS J.O.N.S.")
    text = text.replace("Il. FRANCISCO", "1. FRANCISCO")
    text = text.replace("ESTEBAN\n3.", "ESTEBAN")
    text = text.replace("\n. ", "\n")
    text = text.replace("á.-", "4.-")
    text = text.replace("\nTe ", "\n7.-")
    text = text.replace("\nFJ.", "\n4.")
    text = text.replace("\ndd. RAFAEL", "\n2. RAFAEL")
    text = text.replace("\nHOMBREBUENO COLADO", " HOMBREBUENO COLADO")
    text = text.replace("1i.-", "1.-")
    text = text.replace("SAZ2", "SAZ")
    text = text.replace("Migue)", "Miguel")
    text = text.replace("HARIA:", "MARÍA")
    text = text.replace("REAI:", "REAL")
    text = text.replace("mayc", "mayo")
    text = text.replace("0 A A A e a a A", "")
    text = text.replace("(SUSTAMANTE", "BUSTAMANTE")
    text = text.replace("(RIEGO", "RIEGO")
    text = text.replace("(CASTRO", "CASTRO")
    text = text.replace("\nD. PATRICIO", "\nPATRICIO")
    text = text.replace("is APARICIO", "LUIS ECIJA APARICIO")
    text = text.replace("Bi MARÍA", "6. MARÍA")
    text = text.replace("Sis GREGORIO", "5. GREGORIO")
    text = text.replace("\nTE ANA", "\n11. ANA")
    text = text.replace("\nLa CARMEN", "\n2. CARMEN")
    text = text.replace("- GONZALO PAYO SUBIZA", "5. GONZALO PAYO SUBIZA")
    text = text.replace("Bio MIGUEL", "8. MIGUEL")
    text = text.replace("(GRAJERA", "GRAJERA")
    text = text.replace("TF. JESUS", "7. JESUS")
    text = text.replace("a ANTONIO", "3. ANTONIO")
    text = text.replace("CRU4", "CRUZ")
    text = text.replace("e MARIA", "1. MARIA")
    text = text.replace("No VICENTE", "5. VICENTE")
    text = text.replace("\nY DE LAS AGRUPACIONES IMDENPENDIENTES ESPAÑOLAS", " Y DE LAS AGRUPACIONES INDEPENDIENTES ESPAÑOLAS")
    text = text.replace("GÓME:", "GÓMEZ")
    text = text.replace("6É.-", "6.-")
    text = text.replace("(GONZALEZ", "GONZALEZ")
    text = text.replace("g- MARÍA", "9. MARÍA")
    text = text.replace("CANDIDATURA M g.-", "CANDIDATURA NÚMERO 9.-")
    text = text.replace("\nLa ALFONSA", "\n2. ALFONSA")
    text = text.replace("GARCÍX.", "GARCÍA")
    text = clean_ocr_numbers(text)
    global _CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER
    page_found = False
    for page in range(3343, 3349 + 1):
        if str(page) in text:
            text, _CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER = number_candidates(
                text,
                LOWER_CANDIDATE_NAME_REGEX,
                last_number=_CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER,
            )
            page_found = True
            break
    global _CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER_UPPER
    if not page_found:
        text, _CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER_UPPER = number_candidates(
            text,
            UPPER_CANDIDATE_NAME_REGEX,
            last_number=_CASTILLA_LA_MANCHA_1999_06_LAST_NUMBER_UPPER,
        )
    return text


_CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER = 1


@register_fixer("castilla_la_mancha", 2003, 5)
def fix_castilla_la_mancha_2003_05(text: str) -> str:
    # Remove footer
    if "Y para que así co" in text:
        text = text.split("Y para que así co")[0]
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}:\n", f"CANDIDATURA NÚM. {number}:"
        )
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}\n", f"CANDIDATURA NÚM. {number}:\n"
        )
    # Facilitate parsing
    text = text.replace(
        "IZQUIERDA UNIDA - IZ IERDA D ILLA- MANCHA\n(1.U.)",
        "Candidatura núm. 3: IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA-LA MANCHA (I.U.)",
    )
    text = text.replace(
        "IERRA COMUNERA-PARTID IONALIST",
        "Candidatura núm. 6: TIERRA COMUNERA-PARTIDO NACIONALISTA CASTELLANO",
    )
    # Fix OCR
    text = text.replace("23 de diciembre Electoral", "")
    text = text.replace("N9 3. .- Adolfo Suárez lllana.", "1. Adolfo Suárez Illana.")
    global _CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER
    # Ciudad Real fix
    for page in range(6373, 6379 + 1):
        if str(page) in text:
            text = text.replace(
                "1.- PARTIDO POPULAR", "Candidatura núm. 1: PARTIDO POPULAR"
            )
            text = text.replace(
                "2.- PARTIDO SOCIALISTA OBRERO ESPAÑOL (PSOE",
                "Candidatura núm. 2: PARTIDO SOCIALISTA OBRERO ESPAÑOL (PSOE",
            )
            text = text.replace("3.- LAFALANGE", "Candidatura núm. 3: LA FALANGE")
            text = text.replace(
                "4.- TIERRA COMUNERA", "Candidatura núm. 4: TIERRA COMUNERA"
            )
            text = text.replace("5.- UNIDAD", "Candidatura núm. 5: UNIDAD")
            text = text.replace(
                "IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA-LA MANCHA",
                "Candidatura núm. 6: IZQUIERDA UNIDA - IZQUIERDA DE CASTILLA-LA MANCHA",
            )
            text = text.replace("7.- IZQUIERDA", "Candidatura núm. 7: IZQUIERDA")
            text, _CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER = number_candidates(
                text,
                UPPER_CANDIDATE_NAME_REGEX,
                last_number=_CASTILLA_LA_MANCHA_2003_05_LAST_NUMBER,
            )
    text = clean_ocr_numbers(text)
    return text


@register_fixer("castilla_la_mancha", 2007, 5)
def fix_castilla_la_mancha_2007_05(text: str) -> str:
    text = text.replace("PROVINCIAL\n", "PROVINCIAL ")
    text = text.replace("Provincial de\n", "Provincial de ")
    text = text.replace("IZQUIERDA\n", "IZQUIERDA ")
    text = text.replace("próximo\n", "próximo ")
    text = text.replace("Guadala-\n", "Guadala")
    for number_text, number in NUMBER_MAP.items():
        text = text.replace(
            f"CANDIDATURA NÚMERO {number_text}:\n", f"CANDIDATURA NÚM. {number}:"
        )
    # Fix OCR
    text = clean_ocr_numbers(text)
    text = text.replace("3 DON MANUEL HERNÁNDEZ", "1. DON MANUEL HERNÁNDEZ")
    text = text.replace("4 DON GREGORIO SÁNCHEZ", "1. DON GREGORIO SÁNCHEZ")
    text = text.replace("da. DON JESÚS FERNÁNDEZ", "11. DON JESÚS FERNÁNDEZ")
    text = text.replace("N3 LA FALANGE", "Candidatura núm. 3. LA FALANGE")
    return text


@register_fixer("castilla_la_mancha", 2011, 5)
def fix_castilla_la_mancha_2011_05(text: str) -> str:
    text = text.replace(
        "4. DON DAVID PARDO MOYA\n5. DOÑA MARIA ELENA ESCOBAR GUERRERO\n6. DON PABLO JESUS CANO DURAN",
        "1. DON DAVID PARDO MOYA\n2. DOÑA MARIA ELENA ESCOBAR GUERRERO\n3. DON PABLO JESUS CANO DURAN",
    )
    return text


@register_fixer("castilla_la_mancha", 2015, 5)
def fix_castilla_la_mancha_2015_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "Candidatura núm.: 9. PARTIDO CASTELLANO (PCAS)",
        "Candidatura núm.: 9. PARTIDO CASTELLANO-UNIDAD CASTELLANA (PCAS-UdCA)",
    )
    return text


@register_fixer("castilla_la_mancha", 2023, 5)
def fix_castilla_la_mancha_2023_05(text: str) -> str:
    # Fix dangling suplentes
    text = text.replace("SUPLENTES:\nY para que conste", "")
    return text
