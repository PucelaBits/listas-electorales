import re

from ._common import register_fixer

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


# BOIB 67, err.pdf (Num. 9832): PLIE (candidatura nº 18) Parlament list.
# Erratum: Elisa Crespi Orell is printed in position 1 and Francisco
# Fernández Ochoa in position 2, but the two are swapped (Crespi -> 2,
# Fernández -> 1). The Consell Insular PLIE list in the other file also
# starts with "1. Sra. ELISA CRESPI ORELL", but its position 2 is a
# different name (Antonio Ramos López), so the 4-line anchor holding the
# actual names of positions 1 and 2 is unique to the Parlament list.
@register_fixer("baleares", 2011, 5)
def fix_baleares_2011_05(text: str) -> str:
    text = text.replace(
        "1.\nSra. ELISA CRESPI ORELL\n2.\nSr. FRANCISCO FERNANDEZ OCHOA",
        "1.\nSr. FRANCISCO FERNANDEZ OCHOA\n2.\nSra. ELISA CRESPI ORELL",
    )
    return text
