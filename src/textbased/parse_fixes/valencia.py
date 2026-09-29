import re

from ._common import LOWER_CANDIDATE_NAME_REGEX, UPPER_CANDIDATE_NAME_REGEX, clean_ocr_numbers, fix_maria_ocr, number_candidates, register_fixer


def _fix_valencia_dedouble(text: str) -> str:
    """
    Some of Valencia BO documents are half in Valencian and half in Spanish.
    We remove the Valencian part, which is always first, and keep the Spanish part, which is always second.
    We keep the Spanish part to facilitate the parsing.
    """
    # Look for the last line of the text and search when it appears again
    # If it appears more than twice, we raise an error, because we don't know which one to keep
    last_line = text.splitlines()[-1]
    last_line_count = text.count(last_line)
    if last_line_count > 2:
        raise ValueError(
            f"Last line '{last_line}' appears {last_line_count} times in the text. Cannot dedouble."
        )
    # If it appears only once, we keep the text from the last line onwards
    last_line_index = text.find(last_line)
    text = text[last_line_index + len(last_line) :]
    return text


_VALENCIA_PROVINCE_REGEX = re.compile(
    r"(?i)\b(?:alacant\s*/\s*alicante|alicante\s*/\s*alacant|"
    r"castell[óo]\s*/\s*castell[óo]n|castell[óo]n\s*/\s*castell[óo]|"
    r"val[èe]ncia\s*/\s*valencia|valencia\s*/\s*val[èe]ncia)\b"
)


def _fix_valencia_province(text: str) -> str:
    def replacement(match):
        matched_str = match.group(0).upper()

        # Check which province was matched and return the corresponding string
        if "ALICANTE" in matched_str:
            return "Circunscripción electoral: ALICANTE"
        if "CASTELL" in matched_str:
            return "Circunscripción electoral: CASTELLÓN"
        if "VALEN" in matched_str:
            return "Circunscripción electoral: VALENCIA"

        return match.group(0)

    return re.sub(_VALENCIA_PROVINCE_REGEX, replacement, text)


def _fix_valencia_substitutes(text: str) -> str:
    text = text.replace("\nS1", "\nSUPLENTES\n1.")
    text = text.replace("\nS2", "\nSUPLENTES\n2.")
    text = text.replace("\nS3", "\nSUPLENTES\n3.")
    text = text.replace("\nS4", "\nSUPLENTES\n4.")
    text = text.replace("\nS5", "\nSUPLENTES\n5.")
    text = text.replace("\nS6", "\nSUPLENTES\n6.")
    text = text.replace("\nS7", "\nSUPLENTES\n7.")
    text = text.replace("\nS8", "\nSUPLENTES\n8.")
    text = text.replace("\nS9", "\nSUPLENTES\n9.")
    text = text.replace("\nS10", "\nSUPLENTES\n10.")
    return text


@register_fixer("valencia", 1983, 5)
def fix_valencia_1983_05(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1987, 6)
def fix_valencia_1987_06(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1991, 5)
def fix_valencia_1991_05(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


@register_fixer("valencia", 1995, 5)
def fix_valencia_1995_05(text: str) -> str:
    text = _fix_valencia_province(text)
    return text


_VALENCIA_1999_06_LAST_NUMBER = 1
_VALENCIA_1999_06_LAST_NUMBER_UPPER = 1


@register_fixer("valencia", 1999, 6)
def fix_valencia_1999_06(text: str) -> str:
    # Remove preamble
    if "Elcctoral Provincial de Castollón" in text:
        return "Junta Electoral Provincial de Castellón"
    if "VALENCIANAS a celebrar el próximo dia 13 de junio para" in text:
        return ""
    text = text.replace("ESQUERRA NACIONALISTA VALENCIANA\nPresentación: 4", "Presentación: 4 ESQUERRA NACIONALISTA VALENCIANA")
    text = text.replace("Presentación: ALTERNATIVA.COMUNIDAD VALENCIANA", "Presentación: 7 ALTERNATIVA COMUNIDAD VALENCIANA")
    text = text.replace("IZQUIERDA REPUBLICANA FEDERAL-PARTIDO\n", "IZQUIERDA REPUBLICANA FEDERAL-PARTIDO ")
    text = _fix_valencia_province(text)
    text = text.replace("Carrillo alvárez", "Carrillo Álvarez")
    # Facilitate parsing
    text = text.replace("E Presentación:", "Presentación:")
    text = text.replace("Presentación:", "Candidatura núm:")
    # Duplicate names
    text = text.replace("Antonio Moreno Carrasco\n1", "")
    # Fix OCR
    text = text.replace(" de\n20\nSantos", " de Santos")
    text = text.replace(" de\n", " de ")
    text = text.replace("APELLLIDOS", "APELLIDOS")
    text = text.replace("\n1 Juan\n", "\nJuan ")
    text = text.replace("Rosa Y Saranova", "Rosa María Saranova")
    text = text.replace("Angeles Cabedo l Maliol", "Ángeles Cabedo i Maliol")
    text = text.replace("Jo36", "José")
    text = text.replace("-B.", "-Bautista")
    text = text.replace("Alberto-3.", "Alberto-José")
    text = text.replace("-J.", "-José")
    text = text.replace("-Á.", "-Ángel")
    text = text.replace("-R.", "-Ramón")
    text = text.replace("-l.", "-Isabel")
    text = text.replace("-I.", "-Isabel")
    text = text.replace("yd Julián Jordá Camarasa", "27. Julián Jordá Camarasa")
    text = text.replace("ma Jose-Estebán", "21. José-Estebán")
    text = text.replace("Francisco). Penalva Mompó", "Francisco-José Penalva Mompó")
    text = text.replace("Gonzále:", "González")
    text = text.replace(" cardo", " Cardo")
    text = text.replace("Desamparados-inmaculada\n", "Desamparados-Inmaculada ")
    text = text.replace("M.-Nieves", "María-Nieves")
    text = text.replace("isabel", "Isabel")
    text = text.replace("Maria-M.", "María")
    text = text.replace("tsaboí", "Isabel")
    text = text.replace("isabei", "Isabel")
    text = text.replace("ibarra", "Ibarra")
    text = text.replace("JOsé", "José")
    text = text.replace("Jo0Sé", "José")
    text = text.replace("J0s8", "José")
    text = text.replace("Joz6", "José")
    text = text.replace("logé", "José")
    text = text.replace("Jar A68", "José")
    text = text.replace("méjias", "Mejías")
    text = text.replace(" san ", " San ")
    text = text.replace("ivars", "Ivars")
    text = text.replace("Cale rán", "Caldrán")
    text = text.replace("Sánchez:", "Sánchez")
    text = text.replace("ienor", "Menor")
    text = text.replace("aénimo Hernández Molla", "Jerónimo Hernández Molla")
    text = text.replace("Cslvadar", "Salvador")
    text = text.replace("4 q... en...", "")
    text = text.replace("Jua n AlanGta r Vives", "Juan Blanquer Vives")
    text = text.replace("et 33 aida q", "")
    text = text.replace("e 11 mu o", "")
    text = text.replace("Moltó 1", "Moltó")
    text = text.replace("Déborah P43 FaemnáEI", "Déborah Pascual Fernández")
    text = text.replace("Natividad Y ata Serrano", "Natividad Yuste Serrano")
    text = text.replace("me 2 ta", "")
    text = text.replace("4n an", "Joan")
    text = text.replace("\nL27", "\n27")
    text = text.replace("rais ivorra Gomis", "Luis Ivorra Gomis")
    text = text.replace("Jos9 Ramón Núñez dei 143 011 lO", "José Ramón Núñez del Castillo")
    text = text.replace("de7 Rosa María González González", "Rosa María González González")
    text = text.replace("MaraJUOs", "Marqués")
    text = text.replace("Alain Envlqu a Tar raja", "Alaín Enrique Torroja")
    text = text.replace("José Antonio Belda én1111 Sha", "José Antonio Belda Sánchez")
    text = text.replace("Ser gdiO raira Emo Sanz VÍ va1S10 larn", "Sergio Sanz Valero")
    text = text.replace("Torregr RA", "Torregrosa")
    text = text.replace("A avatin Qánahas Sánrhoz", "Agustín Sánchez Sánchez")
    text = text.replace("E2 Mina Il Rodrianaz Górnez", "Miguel Rodríguez Gómez")
    text = text.replace("A lasé Pe dra Andtán Danans", "José Pedro Antón Conesa")
    text = text.replace("Prieto .:", "Prieto")
    text = text.replace("iváñaz", "Iváñez")
    text = text.replace("N Angeles", "María Ángeles")
    text = text.replace("3046\n", "8046\n")
    text = text.replace("5049\n", "8049\n")
    text = text.replace("3053\n", "8053\n")
    text = text.replace("3059\n", "8059\n")
    text = text.replace("S061\n", "8061\n")
    text = text.replace("3069\n", "8069\n")
    text = text.replace("K)AQUIN", "JOAQUIN")
    text = text.replace("RALUT. ARNAI) MARTINEZ -", "RAUL ARNAIJ MARTINEZ")
    text = text.replace("(ARCÍA", "GARCÍA")
    text = text.replace("(SABEL", "ISABEL")
    text = text.replace("1OSR", "JOSÉ")
    text = text.replace("18 DOGY - Núm. 3.497", "")
    text = text.replace("LLUIS.", "LLUIS")
    text = text.replace("MANEL.", "MANEL")
    text = text.replace("EBR1", "EBRI")
    text = text.replace("Suplentos:", "Suplentes:")
    text = text.replace("2-RMá AIAPIALALO", "ROSARIO")
    text = text.replace("JORGE.", "JORGE")
    text = text.replace("del XAVIER", "33. XAVIER")
    text = text.replace("BTA.", "BAUTISTA")
    text = text.replace("18 ll RO", "")
    text = text.replace("JOSE F)", "JOSE F.")
    text = text.replace("6 1\n", "")
    text = text.replace("M.VICTORIA", "MARÍA VICTORIA")
    text = text.replace("\nPartido Socialista Obrero Español-progresistas", "Partido Socialista Obrero Español-progresistas (PSOE)")
    text = text.replace("134 rd RIA TIRINA\nLISAAA LasGi ALFUUFA ld EN ERAN AA", "Candidatura número 9. Bloc Nacionalista Valencià - Els Verds")
    text = text.replace("INICIATIVA IND EDENDIENTE", "Candidatura número 11. INICIATIVA INDEPENDIENTE")
    text = text.replace("CAESaHER REPUBLICANA FEDERAL-PARTIDO", "Candidatura número 12. IZQUIERDA REPUBLICANA FEDERAL-PARTIDO REPUBLICANO FEDERAL")
    text = text.replace("INAMIPAIEY ACTA 1 1RANA VIA 4 El\nANA 1", "Candidatura número 13. FALANGE ESPAÑOLA DE LAS JONS")
    text = text.replace("YN L-UNIO VALENCIANA\n(UY", "Candidatura número 1. UNIO VALENCIANA (UV)")
    text = text.replace("Ez -E ERKA1 VALE", "Candidatura número 2. ESQUERRA UNIDA PAIS VALENCIA (EUPV)")
    text = text.replace("N3.- COALICIÓN ELECTORAL PSQE", "Candidatura número 3. COALICIÓN ELECTORAL PSOE")
    text = text.replace("N4.- PARTIDO POPULAR", "Candidatura número 4. PARTIDO POPULAR (PP)")
    text = text.replace("95- ALOCON CIO : N\nse\n(LOVERS", "Candidatura número 5. BLOC NACIONALISTA VALENCIA - ELS VERDS (BNV-EV)")
    text = text.replace("o AN VALENCIAS\n(E.N.V.1", "Candidatura número 6. ESQUERRA NACIONALISTA VALENCIANA (ENV)")
    text = text.replace("Ni\n(2.8.", "Candidatura número 7. PARTIDO HUMANISTA (PH)")
    text = text.replace("N8.- IZQUIERDA REPUDLICANA PEDERAL-PARTIDO REPUBLICANO FEDERAL", "Candidatura número 8. IZQUIERDA REPUBLICANA FEDERAL-PARTIDO REPUBLICANO FEDERAL")
    text = clean_ocr_numbers(text)
    global _VALENCIA_1999_06_LAST_NUMBER
    global _VALENCIA_1999_06_LAST_NUMBER_UPPER
    page_found = False
    for page in range(8044, 8074):
        if str(page) in text:
            text = fix_maria_ocr(text)
            text, _VALENCIA_1999_06_LAST_NUMBER = number_candidates(
                text,
                LOWER_CANDIDATE_NAME_REGEX,
                last_number=_VALENCIA_1999_06_LAST_NUMBER,
            )
            page_found = True
            break
    if not page_found:
        text = text.replace(" 1 ", " I ")
        text = fix_maria_ocr(text, upper=True)
        text, _VALENCIA_1999_06_LAST_NUMBER_UPPER = number_candidates(
            text,
            UPPER_CANDIDATE_NAME_REGEX,
            last_number=_VALENCIA_1999_06_LAST_NUMBER_UPPER,
        )
    return text


@register_fixer("valencia", 2003, 5)
def fix_valencia_2003_05(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_substitutes(text)
    return text


@register_fixer("valencia", 2007, 5)
def fix_valencia_2007_05(text: str) -> str:
    # Remove preamble
    if "Anuncio del Ministerio de Fomento" in text:
        return ""
    text = _fix_valencia_province(text)
    text = _fix_valencia_substitutes(text)
    text = text.replace("CADIDATURA", "CANDIDATURA")
    text = text.replace("N.º orden presentación", "Candidatura núm.")
    # TODO: Remove location at the end of the names
    return text


@register_fixer("valencia", 2011, 5)
def fix_valencia_2011_05(text: str) -> str:
    # TODO: err.pdf
    text = _fix_valencia_province(text)
    text = text.replace("Núm. Ord. Pres.", "Candidatura núm.")
    text = text.replace("Nº Ord. Pres:", "Candidatura núm.")
    text = _fix_valencia_substitutes(text)
    return text


@register_fixer("valencia", 2015, 5)
def fix_valencia_2015_05(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_dedouble(text)
    return text


@register_fixer("valencia", 2019, 4)
def fix_valencia_2019_04(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_dedouble(text)
    return text


@register_fixer("valencia", 2023, 5)
def fix_valencia_2023_05(text: str) -> str:
    text = _fix_valencia_province(text)
    text = _fix_valencia_dedouble(text)
    if "MARÍA AMPARO GINER LOZANO" in text:
        # Replace all XX, with XX.
        text = re.sub(r"(\d+),", r"\1.", text)
    return text
