import re

from ._common import register_fixer

P_EXTREMADURA_1995_05 = re.compile(r"^JOSE BAZQUEZ ALVAREZ$", flags=re.MULTILINE)


@register_fixer("extremadura", 1995, 5)
def fix_extremadura_1995_05(text: str) -> str:
    """Corrige el D.O.E. n.º 51 (2.5.1995, p. 1769 col. 2.ª, Acuerdo de
    1.5.1995 de la Junta Electoral Provincial de Badajoz, proclamación de
    candidaturas a la Asamblea de Extremadura) via el D.O.E. n.º 53
    (6.5.1995, p. 1887): CORRECCION de errores.

    Errata única. Candidatura n.º 2 (P.S.O.E.), candidato n.º 11:
    «11 JOSE BAZQUEZ ALVAREZ» -> «11 JOSE VAZQUEZ ALVAREZ» (p. 1769 c2ª =
    c1 p1; nº y nombre en líneas separadas, solo se corrige la línea de
    nombre, única x1 en el corpus).
    """
    return P_EXTREMADURA_1995_05.sub("JOSE VAZQUEZ ALVAREZ", text)

