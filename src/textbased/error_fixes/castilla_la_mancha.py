from ._common import register_fixer


# Diario Oficial de Castilla-La Mancha n.º 84 (30 abr 2015), Corrección de
# errores del Edicto de 27/04/2015, Junta Electoral Provincial de Guadalajara:
#   Candidatura n.º 9, proclamada como "PARTIDO CASTELLANO (PCAS)" debe
#   constar "PARTIDO CASTELLANO-UNIDAD CASTELLANA (PCAS-UdCA)".
#   Se corrige solo la denominación: las líneas de candidatos de esta
#   candidatura no llevan el sufijo "(PCAS)" en el archivo, así que solo la
#   cabecera (única, en candidaturas_4 = Guadalajara) se sustituye.
#   Los paréntesis y el punto se escapan porque la cabecera se busca como
#   patrón regular (en raw string, el acento "ú" se escribe literal).
@register_fixer("castilla_la_mancha", 2015, 5)
def fix_castilla_la_mancha_2015_05(text: str) -> str:
    text = text.replace(
        "Candidatura núm.: 9. PARTIDO CASTELLANO (PCAS)",
        "Candidatura núm.: 9. PARTIDO CASTELLANO-UNIDAD CASTELLANA (PCAS-UdCA)",
    )
    return text
