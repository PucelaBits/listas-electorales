from ._common import register_fixer


# BOA 55, err.pdf (BOA 53, página 1370): Huesca, candidatura nº 3.
# «UNION ARAGONESISTA-CHUNTA ARAGONESISTA» CHA must read «CHUNTA ARAGONESISTA» CHA.
# The scanned text is split across several lines with OCR holes ("UNJON",
# "ARAGONESIST A"); replace each whole chunk with the corrected name only
# (the name as printed in the other provinces).@register_fixer("aragon", 1991, 5)
def fix_aragon_1991_05(text: str) -> str:
    # Summary list of candidaturas (top of the Huesca page)
    text = text.replace(
        "«UNJON\nARAGONESIST A-CHUNT A-\nARAGONESIST A CHA».",
        "«CHUNTA\nARAGONESISTA» CHA.",
    )
    # Candidatura nº 3 header (same page, lower)
    text = text.replace(
        "N.lI 3.-«UNION\nARAGONESISTA-CHUNTA\nARA-\nGONESIST A» CHA",
        "N.lI 3.-«CHUNTA\nARAGONESISTA» CHA",
    )
    return text


# BOA 56, err.pdf (BOA 51, page 1682): Huesca, cant. 2. Izquierda Unida de
# Aragón (IV), suplentes, "1.- Antonia Pedrafita Ferrer" debe decir "1.-
# Antonia Piedrafita Ferrer" (the erratum's "Ferref" is an OCR misread).
@register_fixer("aragon", 1995, 5)
def fix_aragon_1995_05(text: str) -> str:
    # In the scanned PDF the name is in capital letters and the surname is on an
    # independent line ("PEDRAFITA FERRER"), unique in the document.
    text = text.replace("PEDRAFITA FERRER", "PIEDRAFITA FERRER")
    return text


# BOA 67, err.pdf (BOA 62, p. 3042): Huesca, Izquierda Unida de Aragón, titular 8.
@register_fixer("aragon", 1999, 6)
def fix_aragon_1999_06(text: str) -> str:
    # Printed (capitals, em-dash after the number): "8.—MARTA DOLORES CANUDO AZOR"
    text = text.replace("MARTA DOLORES CANUDO AZOR", "MARÍA DOLORES CANUDO AZOR")
    return text


# BOA 54, err.pdf (BOA 50).
@register_fixer("aragon", 2007, 5)
def fix_aragon_2007_05(text: str) -> str:
    # Huesca PSOE cand. 10: Monserrat -> Montserrat (full line, unique).
    text = text.replace(
        "DOÑA MONSERRAT VILLAGRASA ALCANTARA",
        "DOÑA MONTSERRAT VILLAGRASA ALCANTARA",
    )
    # Zaragoza CHA cand. 2: Ibers -> Ibeas
    text = text.replace("NIEVES IBERS VUELTA", "NIEVES IBEAS VUELTA")
    return text
