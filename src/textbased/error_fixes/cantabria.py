from ._common import register_fixer


# BOC 18 (2 may 2007), corrección al BOC extraordinario 17 (1 may 2007),
# JUNTA ELECTORAL PROVINCIAL DE CANTABRIA:
#   Candidatura n.º 11 (Partido Comunista de los Pueblos de España, P.C.P.E.),
#   candidato n.º 37 "IVÁN MARTÍNEZ FERNÁNDEZ" debe decir
#   "IVÁN MARTÍNEZ FERNÁNDEZ - (INDEPENDIENTE)".
#   En el archivo el nombre aparece como "IVAN" (sin tilde) y la línea es
#   única en el documento; el sufijo "- (INDEPENDIENTE)" coincide con el
#   formato ya presente en la suplente 2 de la misma candidatura.
#   (La otra corrección del erratum, la lista de ASTILLERO, es municipal y
#   además solo transcribe "donde dice" sin "debe decir" -> no aplicable.)
# (cantabria usa el prefijo "cna" para no chocar con "can" de canarias)
@register_fixer("cantabria", 2007, 5)
def fix_cantabria_2007_05(text: str) -> str:
    text = text.replace(
        "37. D. IVAN MARTÍNEZ FERNÁNDEZ",
        "37. D. IVAN MARTÍNEZ FERNÁNDEZ - (INDEPENDIENTE)",
    )
    return text
