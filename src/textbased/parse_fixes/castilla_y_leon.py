import re

from ._common import (
    UPPER_DON_CANDIDATE_NAME_REGEX,
    fix_maria_ocr,
    number_candidates,
    register_fixer,
)


@register_fixer("castilla_y_leon", 1983, 5)
def fix_castilla_y_leon_1983_05(text: str) -> str:
    # Errata (err.pdf)
    return text.replace("COALICION PCOE-PCEU", "3. COALICION PCOE-PCEU")


@register_fixer("castilla_y_leon", 1991, 5)
def fix_castilla_y_leon_1991_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "5. Maria Cruz Rodriguez Saldaña.",
        "5. M.ª Cruz Rodríguez Saldaña.",
    )
    text = text.replace(
        "8.- Los Verdes (L.V.)\n1. Raquel Plasencia Diez.",
        "8.- Partido Político Los Verdes (L.V.)\n1. Raquel Plasencia Diez.",
    )
    text = text.replace(
        "2. José María Arribas Moral.",
        "2. José M.ª Arribas Moral.",
    )
    text = text.replace(
        "10.- Centro Democrático y Social (C.D.S.)",
        "10.- Partido Centro Democrático y Social (C.D.S.)",
    )
    text = text.replace(
        "9. Benito de la torre Vega.",
        "9. Benito de la Torre Vega.",
    )
    text = text.replace(
        "3. Dolores Otero Rodríguez de las Heras.",
        "3. M.ª Dolores Otero Rodríguez de las Heras.",
    )
    text = text.replace(
        "10. Fernando Arvizu y Galarraga.",
        "10. Fernando de Arvizu y Galarraga.",
    )
    text = text.replace(
        "15. Natividad Cordero Monrroy.",
        "15. Natividad Cordero Monroy.",
    )
    text = text.replace(
        "10. Maria-Montserrat Alvarez Velasco.",
        "10. María Monserrat Alvarez Velasco.",
    )
    text = text.replace(
        "15. Maria Inmaculada Fuente Villaba.",
        "15. María Inmaculada Fuente Villalba.",
    )
    text = text.replace(
        "5. Antonio de San Mateo Gil.",
        "5. Antonio de Sanmateo Gil.",
    )
    text = text.replace(
        "12. Maria Teresa González Alonso.",
        "12. Teresa González Alonso.",
    )
    text = text.replace(
        "5. Maria Luisa Gavela Ordoñez.",
        "5. María Luisa Gabela Ordóñez.",
    )
    text = text.replace(
        "9. Heliberto López López.",
        "9. Eliberto López López.",
    )
    text = text.replace(
        "1. Carmen Elena Varges López.",
        "1. Carmen Elena Vargues López.",
    )
    text = text.replace(
        "3. Eliseo Garcia Guitiérrez.",
        "3.Eliseo García Gutiérrez.",
    )
    text = text.replace(
        "2.- Partido Politico los Verdes (P.V.)",
        "2.- Partido Politico los Verdes (L.V.)",
    )
    text = text.replace(
        "4. Jacinda Lorenzo Pascua.",
        "4. Jacinta Lorenzo Pascua.",
    )
    text = text.replace(
        "9. Luis Enriquez Espinoza Cuerra.",
        "9. Luis Enrique Espinoza Guerra.",
    )
    text = text.replace(
        "1. Miguel Angel de Diego Nuñez.",
        "1. Miguel Ángel Diego Núñez.",
    )
    text = text.replace(
        "5. Pedro Carlos Acevedo y González.",
        "5. Pedro Carlos Acevedo González.",
    )
    text = text.replace(
        "7. Rafael Vargas Ribera.",
        "7. Rafael Vargas Rivera.",
    )
    text = text.replace(
        "9. Rafael de Diego Nuñez.",
        "9. Rafael Diego Núñez.",
    )
    text = text.replace(
        "2. Maria del Carmen Garcia Rosado y Garcia.",
        "2. María del Carmen García Rosado García.",
    )
    text = text.replace(
        "9. Luis Filguerina Canal.",
        "9. Luis Filgueira Canal.",
    )
    text = text.replace(
        "3. Beatriz Saa y de Corral.",
        "3. Beatriz de Saa Corral.",
    )
    text = text.replace(
        "3.- Unión Castellana (U.C.)",
        "3.- Unión Castellanista (U.C.)",
    )
    text = text.replace(
        "2.- Coalición Izquierda Unida (I.U.)\n1. Alejandro Abad Gil.",
        "2.- Izquierda Unidad (I.U.)\n1. Alejandro Abad Gil.",
    )
    text = text.replace(
        "1. José Oliver Alvarez Seco.",
        "1. José Olivier Álvarez Seco.",
    )
    text = text.replace(
        "4. Maria Isabel Blanca T. Fernández Marassa.",
        "4. M.ª Isabel Blanca T. Fernández Marassa.",
    )
    text = text.replace(
        "6. Javier del Riego Celada.",
        "6. Javier Riego Celada.",
    )
    return text


@register_fixer("castilla_y_leon", 1999, 6)
def fix_castilla_y_leon_1999_06(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("(I.U.-CL)", "(IU-CyL)")
    text = text.replace(
        "1. D. Gabriel Guijosa Allosa.",
        "1. D. Gabriel Guijosa Alloza.",
    )
    text = text.replace("Mª", "María")
    # Facilitate parsing
    text = text.replace("AVILA", "ÁVILA")
    text = text.replace("4.–", "Candidatura núm.: 4.")
    return text


_CYL_2003_05_LAST_NUMBER = 1


@register_fixer("castilla_y_leon", 2003, 5)
def fix_castilla_y_leon_2003_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "D. CASTO GARCÍA GONZÁLEZ\nD. LUIS CASTRO BERROJO",
        "D. LUIS GARCÍA SANZ\nD. CASTO GARCÍA GONZÁLEZ",
    )
    text = text.replace(
        "Dª MIREN JAIONE AVILA ESTEFANÍA",
        "Dª MIREN JAIONE ÁVILA ESTEFANÍA",
    )
    # Remove header
    text = text.replace("Martes, ", "")
    # Facilitate parsing
    text = text.replace("PARTIDO\n", "PARTIDO ")
    text = re.sub(r"(\d+)\.–", r"Candidatura núm.: \1.", text)
    text = fix_maria_ocr(text, upper=True)
    text = text.replace(
        "J U N TA ELECTORAL PROVINCIAL DE VA L L A D O L I D",
        "JUNTA ELECTORAL PROVINCIAL DE VALLADOLID",
    )
    global _CYL_2003_05_LAST_NUMBER
    text, _CYL_2003_05_LAST_NUMBER = number_candidates(
        text,
        UPPER_DON_CANDIDATE_NAME_REGEX,
        last_number=_CYL_2003_05_LAST_NUMBER,
    )
    return text


@register_fixer("castilla_y_leon", 2007, 5)
def fix_castilla_y_leon_2007_05(text: str) -> str:
    # Remove header
    text = text.replace("Martes, ", "")
    # Facilitate parsing
    text = text.replace("\n4.–", "\nCandidatura núm.: 4.")
    text = text.replace("Suplentes: ------", "")
    text = text.replace("N.º 83", "")
    return text


_CYL_2011_05_LAST_NUMBER = None
_CYL_2011_05_CANDIDACY_REGEX = re.compile(r"(\d+)\.\-\s+")


@register_fixer("castilla_y_leon", 2011, 5)
def fix_castilla_y_leon_2011_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("Doña JOSEFA GARCÍA CIRAC", "Doña MARÍA JOSEFA GARCÍA CIRAC")
    text = text.replace(
        "Suplentes:\n1.\nDon EMILIO SANZ AIRAS",
        "Suplentes:\n2.\nDon EMILIO SANTOS AIRAS",
    )
    text = text.replace("Doña FRANCISCO GARCIA MARTIN", "Don FRANCISCO GARCIA MARTIN")
    text = text.replace(
        "Don MARIA DEL CARMEN COSCARON VILLAR",
        "Doña MARIA DEL CARMEN COSCARON VILLAR",
    )
    text = text.replace(
        "Don ALBERTO SERRA BARRERO (PSOE)",
        "Don ALBERTO SERNA BARRERO (PSOE)",
    )
    text = text.replace(
        "Doña ROSA MARIA TERESA DEL CARMEN CARAMANZANA ARAUJO ",
        "Doña ROSA MARÍA TERESA DEL CARMEN CARAMAZANA ARAUJO ",
    )
    # Fix OCR
    text = text.replace("FDEZ.DEL", "FERNANDEZ DEL")
    text = text.replace("JAlONE", "JAIONE")
    text = fix_maria_ocr(text, upper=True)
    text = _CYL_2011_05_CANDIDACY_REGEX.sub(r"Candidatura núm.: \1. ", text)
    # Fix missing candidacy
    text = text.replace(
        "Candidatura núm.: 15. PARTIDO DE CASTILLAY LEON (PCAL)",
        "Candidatura núm.: 14. RELLENO\nNO PROCLAMADA\nCandidatura núm.: 15. PARTIDO DE CASTILLAY LEON (PCAL)",
    )
    global _CYL_2011_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        UPPER_DON_CANDIDATE_NAME_REGEX,
        last_number=_CYL_2011_05_LAST_NUMBER,
    )
    _CYL_2011_05_LAST_NUMBER = last_number
    return text


@register_fixer("castilla_y_leon", 2026, 3)
def fix_castilla_y_leon_2026_03(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "Candidatura núm.: 3. ESPAÑA VACIADA (ESPAÑA VACIADA)",
        "Candidatura núm.: 3. ESPAÑA VACIADA (EV)",
    )
    text = text.replace(
        "4. Doña MARÍA DEL PILAR JUNCO NAVASCUES",
        "4. Doña MARÍA DEL PILAR JUNCO NAVASCUÉS",
    )
    text = text.replace(
        "2. Don AMADOR PARIS CAMINERO",
        "2. Don AMADOR PARÍS CAMINERO",
    )
    text = text.replace(
        "4. Doña NOEMI DORADO MARTINEZ",
        "4. Doña NOEMÍ DORADO MARTÍNEZ",
    )
    text = text.replace(
        "12.Doña ALISSON PLET TEJADA HERRERA",
        "12.Doña ALISSON POLET TEJADA HERRERA",
    )
    text = text.replace(
        "Candidatura núm.: 7. PARTIDO ANIMALISTA CONTRA EL MALTRATO ANIMAL\n(PACMA)",
        "Candidatura núm.: 7. PARTIDO ANIMALISTA CON EL MEDIO AMBIENTE\n(PACMA)",
    )
    return text
