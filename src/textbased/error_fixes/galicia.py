import re

from ._common import register_fixer

P_GALICIA_1997_10_PATTERNS = [
    (
        re.compile(r"Mª Luz Prieto Fernández$", flags=re.MULTILINE),
        "María Luz Prieto Fernández",
    ),
    (
        re.compile(r"^3.– María José Costas Fernández$", flags=re.MULTILINE),
        "3.– Mª José Costas Fernández",
    ),
    (
        re.compile(r"^20.– María José Segade Andrade$", flags=re.MULTILINE),
        "20.– Mª José Segade Andrade",
    ),
    (
        re.compile(r"^9.– Mª de las Mercedes Fortes Costas$", flags=re.MULTILINE),
        "9.– María de las Mercedes Fortes Costas",
    ),
    (
        re.compile(r"^2.– Mª Antonia Pachón Moreno$", flags=re.MULTILINE),
        "2.– María Antonia Pachón Moreno",
    ),
    (
        re.compile(r"^1.– Mª Jesusa Escudero Lago$", flags=re.MULTILINE),
        "1.– María Jesusa Escudero Lago",
    ),
    (
        re.compile(r"OFENSIVA NACIONAL SINDICALISTA \(FGJONS\)$", flags=re.MULTILINE),
        "OFENSIVA NACIONAL SINDICALISTA (F.G. DE LAS JONS)",
    ),
    (
        re.compile(r"^10.– Juan Alfonso Oubina$", flags=re.MULTILINE),
        "10.– Juan Alfonso Oubiña",
    ),
    (
        re.compile(r"^11.– María del Carmen Soliño Castro$", flags=re.MULTILINE),
        "11.– Mª del Carmen Soliño Castro",
    ),
    (
        re.compile(r"^2.– Cándido González Herrero$", flags=re.MULTILINE),
        "2.– Cándido Gonzálvez Herrero",
    ),
]


@register_fixer("galicia", 1997, 10)
def fix_galicia_1997_10(text: str) -> str:
    """Corrige la Resolucción de 22.9.1997 (DOG n.º 183, 23.9.1997, pp.
    9.416-9.425) via la "Corrección de errores" de 22.9.1997 (DOG n.º 191,
    3.10.1997, pp. 9.725-9.726, a instancia de la Junta Electoral Provincial
    de Pontevedra). Candidaturas proclamadas por las Juntas Electorales
    Provinciales de A Coruña, Lugo, Ourense y Pontevedra (elecciones al
    Parlamento de Galicia de 19.10.1997). 10 correcciones:
      p. 9.421 (=candidaturas.pdf p6):
        - PP, supl. n.º 1: "Mª Luz" -> "María Luz" (Prieto Fernández)
        - SDdG, n.º 3: "María José Costas Fernández" -> "Mª José Costas Fernández"
        - Democracia Galega, n.º 20: "María José Segade Andrade" -> "Mª José Segade Andrade"
      p. 9.422 (=p7):
        - P. Humanista, n.º 9: "Mª de las Mercedes Fortes Costas" -> "María de las Mercedes Fortes Costas"
        - P. Humanista, supl. n.º 2: "Mª Antonia Pachón Moreno" -> "María Antonia Pachón Moreno"
        - PSdeG-PSOE, supl. n.º 1: "Mª Jesusa Escudero Lago" -> "María Jesusa Escudero Lago"
        - FGJONS: formación "(FGJONS)" -> "(F.G. DE LAS JONS)" (donde-dice
          la cita como "(FG JONS)"; el archivo imprime "(FGJONS)")
        - FGJONS, n.º 10: "Juan Alfonso Oubina" -> "Juan Alfonso Oubiña"
      p. 9.423 (=p8, Frente Popular Galega):
        - n.º 11: "María del Carmen Soliño Castro" -> "Mª del Carmen Soliño Castro"
        - supl. n.º 2: "Cándido González Herrero" -> "Cándido Gonzálvez Herrero"
          (donde-dice cita la forma del archivo, González; debe-decir añade
          una v: Gonzálvez; la errata lo parte en línea: Gonzál- / vez)
    Guión de lista = en-dash (U+2013); patrones = líneas completas, todas únicas
    (x1) en el corpus.
    """
    for pattern, repl in P_GALICIA_1997_10_PATTERNS:
        text = pattern.sub(repl, text)
    return text


P_GALICIA_2009_03_PATTERNS = [
    (
        re.compile(
            r"^15 Don Juan Francisco Ferreira González[ ]*\n", flags=re.MULTILINE
        ),
        "",
    ),
    (
        re.compile(r"^16 Dona Marta Mascato García *$", flags=re.MULTILINE),
        "15 Dona Marta Mascato García",
    ),
    (
        re.compile(r"^17 Don Antonio Goce Castro *$", flags=re.MULTILINE),
        "16 Don Antonio Goce Castro",
    ),
    (
        re.compile(r"^18 Dona Carmen Ansedes López *$", flags=re.MULTILINE),
        "17 Dona Carmen Ansedes López",
    ),
    (
        re.compile(r"^19 Don Rafael Blanco Guerreiro *$", flags=re.MULTILINE),
        "18 Don Rafael Blanco Guerreiro",
    ),
    (
        re.compile(r"^20 Dona Begoña Domínguez Táboas *$", flags=re.MULTILINE),
        "19 Dona Begoña Domínguez Táboas",
    ),
    (
        re.compile(r"^21 Dona María Ángeles Conde Salgado *$", flags=re.MULTILINE),
        "20 Dona María Ángeles Conde Salgado",
    ),
    (
        re.compile(r"^22 Don José María Tobío Barreira *$", flags=re.MULTILINE),
        "21 Don José María Tobío Barreira",
    ),
]


@register_fixer("galicia", 2009, 3)
def fix_galicia_2009_03(text: str) -> str:
    """Corrige la Resolución de 27 de enero de 2009 (DOG n.º 23,
    3.2.2009, pp. 2.283-2.294), que publicó las candidaturas
    presentadas en las Juntas Electorales Provinciales de A Coruña, Lugo,
    Ourense y Pontevedra (elecciones al Parlamento de Galicia, Real
    decreto 1/2009, de 5.1.2009), mediante el Acuerdo de 24 de febrero de
    2009 [sic: la errata reza "2008"] de la Junta Electoral Provincial
    de Pontevedra (DOG n.º 40, 26.2.2009, p. 4.077; expediente
    electoral AP-42). Renuncia de Juan Francisco Ferreira González (DNI
    36099338-X), candidato n.º 15 de la candidatura del PSdeG-PSOE a
    Pontevedra: eliminada la línea del n.º 15 y renumeración "en
    sentido ascendente" de los titulares posteriores (16-22 -> 15-21); los
    suplentes (n.ºs 1-5) conservan su numeración. Ignoradas (no
    electorales, fuera de este archivo): correccién del art. 7.7 (p.
    2.946), nombramiento de tribunal (Consellería de Presidencia,
    p. 4.077) y composicién de comisiones de la Consellería de
    Educación. NOTAS: el encabezado de las páginas de 2009 lleva
    un control U+0002 tras "Nº 23" (nunca anclar en el encabezado); la
    separación n.º/nombre es un espacio simple (no en-dash, a
    diferencia de 1997); cada línea lleva un espacio final, por eso los
    patrones de renumeración anclan "^<num> <nombre>" sin "$" y la
    eliminación traga el espacio final. Patrones xúnicos (x1) en el
    corpus de 12 páginas: los titulares 15-21 de UPyD, PP, PH u otras
    listas comparten n.ºs, y el nombre completo ancla la línea."""
    for pattern, repl in P_GALICIA_2009_03_PATTERNS:
        text = pattern.sub(repl, text)
    return text
