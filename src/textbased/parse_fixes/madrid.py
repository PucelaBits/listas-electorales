import re

from common import NAME_WHITELIST_CHARS

from ._common import register_fixer

_MADRID_INVERSE_CANDIDACY_REGEX = re.compile(
    rf"^([{NAME_WHITELIST_CHARS}\d \(\)\+\.’]+)[\r?\n]+(Candidatura número[:|\.]? \d+\.?)$",
    re.MULTILINE,
)


def _madrid_inverse_candidacy_fix(text: str) -> str:
    for match in _MADRID_INVERSE_CANDIDACY_REGEX.finditer(text):
        # We want to invert it so it is "Candidatura número: X" followed by the name
        text = text.replace(match.group(0), match.group(2) + " " + match.group(1))
    return text


@register_fixer("madrid", 1995, 5)
def fix_madrid_1995_05(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 1999, 6)
def fix_madrid_1999_06(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2003, 5)
def fix_madrid_2003_05(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2003, 10)
def fix_madrid_2003_10(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2007, 5)
def fix_madrid_2007_05(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2011, 5)
def fix_madrid_2011_05(text: str) -> str:
    # Remove header
    if "Candidaturas proclamadas por los diversos partidos políticos y coaliciones que" in text:
        return "Circunscripción electoral de Madrid"
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2015, 5)
def fix_madrid_2015_05(text: str) -> str:
    # TODO: Errata (err.pdf)
    text = text.replace(
        "Don Gonzalo Martín García (DEMOCRACIA NACIONAL)",
        "Don Gonzalo Martín García (DEMOCRACIA NACIONAL)\n108. Doña Adelina Valverde Zabala (LA FALANGE-FE)\n109. Doña Marta Beatriz Fernández Fernández (LA FALANGE-FE)\n110. Doña Susana Agraz Cazaña (Independiente)\n111. Don Sergio García Rubio (LA FALANGE-FE)\n112. Don Ángel Mañas Pérez (LA FALANGE- FE)\n113. Doña Dolores Magro Martínez (LA FALANGE-FE)\n114. Doña Raquel Vicente-Ruiz Aguilar (Independiente)\n115. Doña Gemma Sainz Bonilla (LA FALANGE-FE)\n116. Don Faustino Fuentes Álvarez (LA FALANGE-FE)\n117. Don Carlos Javier Rodríguez Muñoz (LA FALANGE-FE)\n118. Doña María Magdalena Carbajo Serrano (DEMOCRACIA NACIONAL)\n119. Don Sergio Felipe Benavente (LA FALANGE-FE)\n120. Doña María Alejandra Alonso Pardo (Independiente)\n121. Don Nemesio Cabezuela Varela (LA FALANGE-FE)\n122. Don Camilo Luis Rodríguez Fraile (LA FALANGE-FE)\n123. Don José López García (LA FALANGE-FE)\n124. Doña Carmen Lobo Pérez (LA FALANGE-FE)\n125. Doña Lucía Maroto Cuenca (LA FALANGE-FE)\n126. Don Gonzalo Chicharro Lamamie de Clairac (MOVIMIENTO CATÓLICO ESPAÑOL)\n127. Don Fernando Maqueda Jiménez (LA FALANGE-FE)\n128. Doña Marleny Morales Marichal (LA FALANGE-FE)\n129. Doña María Teresa de Jesús San Román Bachiller (DEMOCRACIA NACIONAL)",
    )
    text = text.replace("\xad", "-")
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2019, 5)
def fix_madrid_2019_05(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text


@register_fixer("madrid", 2021, 5)
def fix_madrid_2021_05(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    if "Isabel Natividad Díaz Ayuso" in text:
        # Remove excluded candidates
        text = text.replace("5. Toni Cantó García del Moral (Independiente)\n", "")
        text = text.replace("23. Agustín Conde Bajén\n", "")

        # Shift numbering for candidates originally placed 24 to 73 (shift down by 2)
        # Iterating in descending order to avoid overwriting numbers we just updated
        for i in range(73, 23, -1):
            text = text.replace(f"{i}. ", f"{i - 2}. ", 1)

        # Shift numbering for candidates originally placed 6 to 22 (shift down by 1)
        for i in range(22, 5, -1):
            text = text.replace(f"{i}. ", f"{i - 1}. ", 1)
    elif "Ignacio Catalá Martínez" in text:
        # Shift numbering for candidates originally placed 72 to 136 (shift down by 2)
        # Iterating in descending order to avoid overwriting numbers we just updated
        for i in range(136, 71, -1):
            text = text.replace(f"{i}. ", f"{i - 2}. ", 1)
        # Restructure the Suplentes section into the main list
        text = text.replace(
            "Suplentes\n1. Inés Espada Sanchís\n2. Alfonso Javier Muñoz Casares\n3. Natalia Rey Riveiro",
            "135. Inés Espada Sanchís\n136. Alfonso Javier Muñoz Casares\nSuplente\n1. Natalia Rey Riveiro",
        )
    return text


@register_fixer("madrid", 2023, 5)
def fix_madrid_2023_05(text: str) -> str:
    text = _madrid_inverse_candidacy_fix(text)
    return text
