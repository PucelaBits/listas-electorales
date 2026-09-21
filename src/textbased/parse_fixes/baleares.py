import re

from ._common import register_fixer

_BOIB_REGEX = re.compile(r"^.*BOIB.*$", re.MULTILINE)

def _baleares_province_fix(text: str) -> str:
    suffix = 1
    if "consejos insulares" in text.lower():
        suffix = 10
    text = text.replace("Mallorca\n", f"BALE-{suffix}\n")
    text = text.replace("MALLORCA\n", f"BALE-{suffix}\n")
    text = text.replace("Ibiza\n", f"BALE-{suffix + 1}\n")
    text = text.replace("IBIZA\n", f"BALE-{suffix + 1}\n")
    text = text.replace("Eivissa\n", f"BALE-{suffix + 1}\n")
    text = text.replace("EIVISSA\n", f"BALE-{suffix + 1}\n")
    text = text.replace("Menorca\n", f"BALE-{suffix + 2}\n")
    text = text.replace("MENORCA\n", f"BALE-{suffix + 2}\n")
    text = text.replace("Formentera\n", f"BALE-{suffix + 3}\n")
    text = text.replace("FORMENTERA\n", f"BALE-{suffix + 3}\n")
    text = text.replace("Sant Antoni de Portmany\n", f"BALE-{suffix + 4}\n")
    text = text.replace("Sant Josep de sa Talaia\n", f"BALE-{suffix + 5}\n")
    text = text.replace("Sant Joan de Labritja\n", f"BALE-{suffix + 6}\n")
    text = text.replace("Santa Eulària des Riu\n", f"BALE-{suffix + 7}\n")
    return text


# BOCA 58, err.pdf (BOCA 55, pp. 3452-3454). Six corrections; this PDF's OCR
# breaks most rows into separate "number" and "name" lines, so only the
# name-level corrections can be applied with a text fixer.
# NOT POSSIBLE: Menorca PSOE, candidates 14-16 "are suplentes" — that only
# works as a "Suplentes" marker-line insertion, which would also reclassify
# the following (Unió Progressista) candidates as substitutes. Flagged for
# manual review.
P_BALEARES_1991_05 = re.compile(r"José Pedraza Pérez\s+suplentes")


@register_fixer("baleares", 1991, 5)
def fix_baleares_1991_05(text: str) -> str:
    # p3452 Mallorca U.I.M. cand. 32
    text = text.replace("Luis Marín Pallas", "Antonio Durán Cañellas")
    # p3453 Menorca EEM cand. 10 (OCR split the surname into "Llofri u")
    text = text.replace("Llofri u", "Llufriu")
    # p3453 Menorca Unió Progressista cand. 2
    text = text.replace("Catalina Serar Tur", "Catalina Serra Tur")
    # p3453 Menorca Unió Progressista cand. 11: the OCR prints an extra
    # lowercase "suplentes" right after the name (a stray line); the real
    # "Suplents/Suplentes" marker of this candidacy is printed further down.
    # Delete the stray one.
    text = P_BALEARES_1991_05.sub("José Pedraza Pérez", text)
    # p3454 Ibiza-Formentera Fed. Independientes cand. 2 (OCR: "Uobet" for
    # "Llobet"). The Catalan erratum says "Mariano" but the Spanish one says
    # "Mariana" (printed "Marinao"); following the Catalan (primary) reading.
    text = text.replace("Marinao Uobet Roman", "Mariano Llobet Roman")
    # p3454 Ibiza-Formentera ENE suppl. 2 (OCR: "Isael")
    text = text.replace("Isael Ferrer Arabi", "Isabel Ferrer Arabi")
    return text

_BALEARES_2007_05_FIRST_1_SUBSTITUTE_REGEX = re.compile(r"^1 (.+) Suplente$", re.MULTILINE)
_BALEARES_2007_05_FIRST_34_SUBSTITUTE_REGEX = re.compile(r"^34 (.+) Suplente$", re.MULTILINE)
_BALEARES_2007_05_REPEAT_FIRST_SUBSTITUTE_REGEX = re.compile(r"^Suplente nº 1(.+)$", re.MULTILINE)

@register_fixer("baleares", 2007, 5)
def fix_baleares_2007_05(text: str) -> str:
    # Remove preamble
    if "Consorcio, para cumplir sus finalidades, puede realiz" in text:
        return ""
    if "Consorci, per acomplir les seves finalitats" in text:
        text = text.split("Consorci, per acomplir les seves finalitats")[-1]
    text = text.replace("UNIÓ CENTRISTES DE MENORCA\n", "UNIÓ CENTRISTES DE MENORCA (UCM)\n")
    text = _baleares_province_fix(text)
    text = text.replace("Nº Candidato/a Formación Política", "")
    text = text.replace("Nº Candidato/a\nFormación Política", "")
    text = text.replace("Num ", "Candidatura núm. ")
    text = text.replace("Num7", "Candidatura núm. 7")
    # Remove lines that contain BOIB
    text = _BOIB_REGEX.sub("", text)
    # Replace the first substitute line
    text = _BALEARES_2007_05_FIRST_1_SUBSTITUTE_REGEX.sub(r"Suplentes\n1 \1", text)
    text = _BALEARES_2007_05_FIRST_34_SUBSTITUTE_REGEX.sub(r"Suplentes\n34 \1", text)
    text = _BALEARES_2007_05_REPEAT_FIRST_SUBSTITUTE_REGEX.sub(r"Suplentes\n1 \1", text)
    text = text.replace(" Suplente", "")
    text = text.replace("Suplente nº ", "")
    text = text.replace("34 Sra. Laura Maria Bryant Forteza Independiente", "SUPLENTES\n34 Sra. Laura Maria Bryant Forteza")
    text = text.replace("34 Sr. Mateo Morro Latorre", "SUPLENTES\n34 Sr. Mateo Morro Latorre")
    text = text.replace("PARTIDO SOCIALISTA OBRERO\n", "PARTIDO SOCIALISTA OBRERO ")
    text = text.replace("2\n3 DON JAVIER ABRIL DE COO\nDOÑA MARIA JESUS MATA RODILANA", "2 DON JAVIER ABRIL DE COO\n3 DOÑA MARIA JESUS MATA RODILANA")
    # Missing candidacies
    text = text.replace("\nPARTIDO POPULAR", "\nCandidatura núm. 1 PARTIDO POPULAR")
    text = text.replace("\nPARTIDO SOCIALISTA OBRERO ESPAÑOL", "\nCandidatura núm. 2 PARTIDO SOCIALISTA OBRERO ESPAÑOL")
    text = text.replace("\nESQUERRA DE MENORCA-ESQUERRA UNIDA", "\nCandidatura núm. 3 ESQUERRA DE MENORCA-ESQUERRA UNIDA")
    text = text.replace("\nCOALICIÓ ELECTORAL PARTIT SOCIALISTA DE MENORCA-ENTESA", "\nCandidatura núm. 4 COALICIÓ ELECTORAL PARTIT SOCIALISTA DE MENORCA-ENTESA")
    text = text.replace("\nUNIÓ CENTRISTES DE MENORCA", "\nCandidatura núm. 5 UNIÓ CENTRISTES DE MENORCA")
    text = text.replace("\nCIUDADANOS EN BLANCO", "\nCandidatura núm. 6 CIUDADANOS EN BLANCO")
    return text


@register_fixer("baleares", 2011, 5)
def fix_baleares_2011_05(text: str) -> str:
    text = _baleares_province_fix(text)
    # Errata (err.pdf)
    text = text.replace(
        "1.\nSra. ELISA CRESPI ORELL\n2.\nSr. FRANCISCO FERNANDEZ OCHOA",
        "1.\nSr. FRANCISCO FERNANDEZ OCHOA\n2.\nSra. ELISA CRESPI ORELL",
    )
    # Remove lines that contain BOIB
    text = _BOIB_REGEX.sub("", text)
    text = text.replace("Orden Nombre y apellidos", "")
    return text


@register_fixer("baleares", 2015, 5)
def fix_baleares_2015_05(text: str) -> str:
    text = _baleares_province_fix(text)
    return text


@register_fixer("baleares", 2019, 5)
def fix_baleares_2019_05(text: str) -> str:
    # Remove zero-width space characters (U+200B)
    text = text.replace("\u200b", "")
    text = text.replace(
        "Fascículo 89 - Sec. V. - Pág. 17702",
        "Fascículo 89 - Sec. V. - Pág. 17702\nElecciones a los Consejos Insulares de 2019",
    )
    text = text.replace(
        "Fascículo 89 - Sec. V. - Pág. 17737",
        "Fascículo 89 - Sec. V. - Pág. 17737\nElecciones a los Consejos Insulares de 2019",
    )
    text = _baleares_province_fix(text)
    # Fix error
    text = text.replace(
        "4. JUAN FRANCISCO TORRES SERRA", "3. JUAN FRANCISCO TORRES SERRA"
    )
    return text


@register_fixer("baleares", 2023, 5)
def fix_baleares_2023_05(text: str) -> str:
    text = _baleares_province_fix(text)
    return text
