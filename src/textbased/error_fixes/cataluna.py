import re

from ._common import register_fixer


@register_fixer("cataluna", 1999, 10)
def fix_cataluna_1999_10(text: str) -> str:
    """Corrección de erratas (DOGC n.º 2981, 23-09-1999, p. 12552-3) del edicto
    de 20-09-1999 con la lista de candidaturas proclamadas al Parlamento de
    Catalunya 1999 por la Junta Electoral Provincial de BARCELONA
    (DOGC n.º 2979, 21-09-1999, p. 12431-12438).

    candidaturas_1.pdf contiene las páginas 12431-12438 (los otros tres PDFs
    son las páginas de otras provincias del mismo DOGC: 12438-12444); todas
    las erratas caen en candidaturas_1.pdf:
      - p. 12433 = candidatura núm. 7 (Barcelona I)
      - p. 12436 = candidatura núm. 14 (Barcelona II / CIPC-… según la
        errata, corre la misma página)

    Formato del archivo: cada candidato es un bloque de 2 líneas
    ("Nº" + nombre); los "donde dice"/"debe decir" de la errata citan ambas
    líneas en un solo renglón ("4 Jose…") — se ancla "número\\nnombre" y solo
    se reescribe la línea del nombre.

    1. "1\\nPascual Maragall i Mira" -> "1\\nPasqual Maragall i Mira"
       (P y a intercambiados).
    2. "4\\nJose Mª Vallés i Casadevall (CIPC)" -> "4\\nJosep M. Vallés i
       Casadevall (CIPC)". (La errata cita el "donde dice" como "Valles"
       sin acento, pero el BOC ya llevaba "Vallés" con acento: se conserva el
       acento del archivo y se aplica solo el "Josep M." de la errata.)
    3. "76\\nJordi Lozano Gonzalez (Petit) (CIPC)" -> "76\\nJordi Lozano
       Gonzalez (Jordi Petit) (CIPC)" (el apodo va precedido del nombre).
    4. "8\\nIgansi Riera Gassiot" -> "8\\nIgnasi Riera Gassiot".
    5. "18\\nJudith Cobachos Haya" -> "18\\nJudith Cobacho Haya".
    6. "41\\nÀngela Morillo Maymón" -> "41\\nÀngels Morillo Maymón" (femenino
       plural).
    7. "56\\nMarga Maldonado Rubio" -> "56\\nMargarida Maldonado Rubio".
    8. "82\\nMaria Luisa López Pérez" -> "82\\nMaria Lluïsa López Pérez".
    9. Suplentes de la misma candidatura: "Suplentes:\\n1\\nGerard Gual
       Gasulla\\n2\\nMaria Luisa Martos Cerrillo" -> "…\\n2\\nMaria Lluïsa
       Martos Cerrillo" (la errata omite la suplente 1 en su cita; se ancla el
       bloque completo para singularizar el "2").
    """
    text = text.replace("1\nPascual Maragall i Mira", "1\nPasqual Maragall i Mira")
    text = text.replace(
        "4\nJose Mª Vallés i Casadevall (CIPC)",
        "4\nJosep M. Vallés i Casadevall (CIPC)",
    )
    text = text.replace(
        "76\nJordi Lozano Gonzalez (Petit) (CIPC)",
        "76\nJordi Lozano Gonzalez (Jordi Petit) (CIPC)",
    )
    text = text.replace("8\nIgansi Riera Gassiot", "8\nIgnasi Riera Gassiot")
    text = text.replace("18\nJudith Cobachos Haya", "18\nJudith Cobacho Haya")
    text = text.replace("41\nÀngela Morillo Maymón", "41\nÀngels Morillo Maymón")
    text = text.replace("56\nMarga Maldonado Rubio", "56\nMargarida Maldonado Rubio")
    text = text.replace("82\nMaria Luisa López Pérez", "82\nMaria Lluïsa López Pérez")
    text = text.replace(
        "Suplentes:\n1\nGerard Gual Gasulla\n2\nMaria Luisa Martos Cerrillo",
        "Suplentes:\n1\nGerard Gual Gasulla\n2\nMaria Lluïsa Martos Cerrillo",
    )
    return text


P_CATALUNA_2003_11_1 = re.compile(
    r"Candidatura n[uú]m\. 3\nFormaci[oó]n pol[ií]tica: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi \(PSC-CpC\)"
)
P_CATALUNA_2003_11_2 = re.compile(
    r"Candidatura n[uú]m\. 2\nFormaci[oó]n pol[ií]tica: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi \(PSC-CpC\)"
)
P_CATALUNA_2003_11_3 = re.compile(
    r"Candidatura n[uú]m\. 18\nFormaci[oó]n pol[ií]tica: Estat Català\n1\nJordi Miro i Riba"
)
P_CATALUNA_2003_11_4 = re.compile(
    r"16\nMar[ií]a Teresa Vinuesa L[oó]pez \(Estat Català\)"
)


@register_fixer("cataluna", 2003, 11)
def fix_cataluna_2003_11(text: str) -> str:
    """Corrección de erratas (DOGC n.º 3994, 23-10-2003, p. 20878) del edicto
    de 20-10-2003 del DOGC n.º 3992 (21-10-2003, p. 20321-20335) con las listas
    de candidaturas proclamadas al Parlamento de Cataluña 2003.

    Tres erratas, una por provincia. El DOGC 3994 contiene además anuncios
    judiciales/JEZ sin erratas; solo se tocan los candidatos de las
    provincias que citan la errata (Barcelona, Tarragona, Lleida):
      - Barcelona (03.295.062): p. 20321-20329 (candidaturas_1.pdf p0-p8; la
        p. 20329 se duplica en candidaturas_2.pdf p0).
      - Tarragona (03.295.052): p. 20333 (candidaturas_3.pdf p2 = duplicado
        en candidaturas_4.pdf p0).
      - Lleida (03.295.050): p. 20332 (candidaturas_3.pdf p1).

      1. Tarragona, cand. 3 (PSC - Ciutadans pel Canvi): la segunda línea de
         formación, "…(PSC-CpC)" -> "…(PSC (PSC-PSOE) - CpC)". OJO: la errata
         cita el "donde dice" como "(PSC- CpC)" (con espacio tras el guion)
         pero el archivo NO lleva ese espacio — se ancla por las 3 líneas del
         encabezado (único; la p. 20333 se duplica en c3p2/c4p0 y en ambas
         páginas se aplica).
      2. Barcelona, cand. 2 (mismo partido): "…(PSC-CpC)" ->
         "…(PSC (PSC-PSOE)-CpC)" (ahí la errata sí cita el "donde dice" igual
         que el archivo).
      3. Barcelona, cand. 18 (Estat Català): la línea de formación
         "Formación política: Estat Català" -> "… (EC)" ("deben figurar las
         siglas 'EC'"); se ancla el bloque de 4 líneas con "Candidatura núm.
         18" + nº1 (único en c1p8 y su duplicado c2p0; hay otros "Estat
         Català" sin sigla del edicto de Girona, p. 20331, y otros con "(EC)"
         ya — Tarragona).
      4. Lleida, cand. 10 (Estat Català): "16\nMaría Teresa Vinuesa López
         (Estat Català)" -> "Suplente:\n1\nMaría Teresa Vinuesa López (Estat
         Català)" — el "donde dice" cita "16" y el "debe decir" cita el bloque
         "Suplente:/1/María…" (la persona pasa de ser candidata nº16 a ser la
         suplente nº1; el renumerado a "1" es parte de la errata). OJO: el "16"
         va DESPUÉS de la lista completa 1-15 (no justo bajo el encabezado),
         así que el ancla es solo el par "16\nMaría…" (único). +1 línea en
         p. 20332 (intencional).
    """
    text = P_CATALUNA_2003_11_1.sub(
        "Candidatura núm. 3\nFormación política: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi (PSC (PSC-PSOE) - CpC)",
        text,
    )
    text = P_CATALUNA_2003_11_2.sub(
        "Candidatura núm. 2\nFormación política: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi (PSC (PSC-PSOE)-CpC)",
        text,
    )
    text = P_CATALUNA_2003_11_3.sub(
        "Candidatura núm. 18\nFormación política: Estat Català (EC)\n1\nJordi Miro i Riba",
        text,
    )
    text = P_CATALUNA_2003_11_4.sub(
        "Suplente:\n1\nMaría Teresa Vinuesa López (Estat Català)", text
    )
    return text


P_CATALUNA_2006_11_PATTERNS = [
    (
        re.compile(r"^13\. Josep Maria Freixenet i Mayans", flags=re.MULTILINE),
        "13. Josep Maria Freixanet i Mayans",
    ),
    (
        re.compile(r"^44\. Ant[oò]nia Serra i Baucells", flags=re.MULTILINE),
        "44. Antònia Serra i Baucells (Independent)",
    ),
    (
        re.compile(r"^3\. Xavier Vinyals i Capdepon", flags=re.MULTILINE),
        "3. Xavier Vinyals i Capdepon (Independent)",
    ),
    (
        re.compile(
            r"^35\. Jos[eé] Antonio Garc[ií]a Balllester \(Ind\)", flags=re.MULTILINE
        ),
        "35. José Antonio García Ballester (Ind)",
    ),
    (
        re.compile(r"^6\. Abert Camarasa Escubedo", flags=re.MULTILINE),
        "6. Albert Camarasa Escubedo",
    ),
    (
        re.compile(r"^70\. Monserrat Cervera Casanueva", flags=re.MULTILINE),
        "70. Montserrat Cervera Casanueva",
    ),
    (
        re.compile(r"^38\. Maria de la torre i Prieto", flags=re.MULTILINE),
        "38. Maria de la Torre i Prieto",
    ),
    (
        re.compile(
            r"^1\. Francesc Corbella Valea\n"
            r"2\. Maria Dolors Ivorra Cano\n"
            r"3\. Rafael Lopez Urgel\n"
            r"4\. Eva Maria [AÁ]lvarez Moya\n"
            r"5\. V[ií]ctor Abella Salido\n"
            r"6\. Alexandra Fernandez Ruiz\n"
            r"7\. Graciela Medina Esquivel\n"
            r"8\. Damaris Moran Perez\n"
            r"9\. Pedro Garrote Vilchez\n"
            r"10\. Maria Cinta Escriche Matheu\n"
            r"11\. Gerard Font Izquierdo\n"
            r"12\. Ana Artazcoz Sastre\n"
            r"13\. Xavier Frias Roman\n"
            r"14\. Yasmina Andujar Vazquez\n"
            r"15\. Jos[eé] Manuel Gomez Arribas\n"
            r"16\. Maria Lucia Jurado Pouso\n"
            r"17\. Francisca Jimenez Cozar",
            flags=re.MULTILINE,
        ),
        (
            "1. Francesc Corbella Valea\n"
            "2. Maria Dolors Ivorra Cano\n"
            "3. Rafael Lopez Urgel\n"
            "4. Eva Maria Álvarez Moya\n"
            "5. Víctor Abella Salido\n"
            "6. Graciela Medina Esquivel\n"
            "7. Pedro Garrote Vilchez\n"
            "8. Maria Cinta Escriche Matheu\n"
            "9. Gerard Font Izquierdo\n"
            "10. Xavier Frias Roman\n"
            "11. Yasmina Andujar Vazquez\n"
            "12. José Manuel Gomez Arribas\n"
            "13. Maria Lucia Jurado Pouso\n"
            "14. Francisca Jimenez Cozar\n"
            "15. Anahí Aradas Medina\n"
            "16. Gloria Folguera Ventura\n"
            "17. Xavier Ortiz Forns"
        ),
    ),
]


@register_fixer("cataluna", 2006, 11)
def fix_cataluna_2006_11(text: str) -> str:
    """Rectifica el DOGC núm. 4735 (6.10.2006) via el DOGC núm. 4737 (10.10.2006,
    p. 42414): candidaturas proclamadas al Parlamento de Catalunya (2006).
    Dos edictos de rectificación: Junta Electoral Provincial de BARCELONA
    (06.279.125, firmas ilegibles) y de GIRONA (06.282.001, Roser Gusiñer).

    BARCELONA (p. 42025-42033):
      1. cand. 3 ERC (06.279.125): "13. Josep Maria Freixenet i Mayans" ->
         "Freixanet" (la errata cita "FREIXANET" en mayúsculas; el archivo usa
         mayúscula-inicial, así que se corrige solo el grafismo en su estilo).
      2. cand. 3 ERC, candidata 44: "44. Antònia Serra i Baucells" -> añadir la
         denominación de independiente. El bloque ERC no lleva NINGUNA etiqueta,
         así que se añade la forma de palabra completa "(Independent)" que usa
         el edicto catalán (la errata dice "la denominació INDEPENDENT", la
         palabra completa, no la abreviatura "(Ind)"). JUICIO: se elige
         "(Independent)" sobre "(Ind)".
      3. cand. 3 ERC, suplente 3: "3. Xavier Vinyals i Capdepon" -> añadir
         "(Independent)" (mismo criterio que el punto 2).
      4. cand. 7 Ei (06.279.125): "35. José Antonio García Balllester (Ind)" ->
         "Ballester" (la errata cita "BALLESTER" en mayúsculas; solo el grafismo).
      5. cand. 8 PCPC (06.279.125): "6. Abert Camarasa Escubedo" -> "Albert"
         (mayúsculas en la errata; solo el grafismo).
      6. cand. 12 PFiV (06.279.125): "70. Monserrat Cervera Casanueva" ->
         "Montserrat".
      7. cand. 13 EV-EVC (06.279.125): "38. Maria de la torre i Prieto" ->
         "de la Torre".

    GIRONA (p. 42033-42036):
      8. cand. 10 POR UN MUNDO MÁS JUSTO (PUM+J) (06.282.001): "ha de constar de
         la següent manera" + bloque de 17 nombres renumerado. La errata RETIRA
         3 nombres del archivo (n.º6 Alexandra Fernandez Ruiz, n.º8 Damaris Moran
         Perez, n.º12 Ana Artazcoz Sastre) y AÑADE 3 nuevos al final (15. Anahí
         Aradas Medina, 16. Gloria Folguera Ventura, 17. Xavier Ortiz Forns),
         renumerando el resto. Se sustituye el bloque completo de 17 líneas del
         encabezado (1. Francesc...17. Francisca) por el bloque corregido.
         -1/+3 (línea por línea casi toda la cola cambia por el renumerado).

    NO POSIBLE (no se aplica):
      9. cand. 11 (06.282.001): "La denominació ... núm. 11 ha de constar de la
         següent manera: Escons insubmisos - Alternativa dels Demòcrates
         Descontents (Ei)". El archivo YA lleva esa denominación en el estilo de
         mayúsculas del edicto: "PARTIT: ESCONS INSUBMISOS - ALTERNATIVA DELS /
         DEMÒCRATES DESCONTENTS (Ei)" (idéntico letra a letra, solo cambia la
         caja y el prefijo "PARTIT:"). Todas las líneas PARTIT/FEDERACIÓ/COALICIÓ
         del edicto de Girona van en MAYÚSCULAS, así que la cita en mixto de la
         errata es solo la forma canónica; no hay delta textual que sustituir.
         No se reescribe caja (sería "mejorar" más allá de la errata).
    """
    for pattern, repl in P_CATALUNA_2006_11_PATTERNS:
        text = pattern.sub(repl, text)
    return text


@register_fixer("cataluna", 2010, 11)
def fix_cataluna_2010_11(text: str) -> str:
    """Corrige el DOGC núm. 5746 (2.11.2010) via el DOGC núm. 5749 (5.11.2010,
    p. 81517): "Edicto de 2 de noviembre de 2010, por el que se hace pública la
    corrección de una errata en el Edicto de 1 de noviembre de 2010, de la Junta
    Electoral Provincial de Lleida (DOGC núm. 5746, pág. 80144, de 2.11.2010)".

    Errata única. LLEIDA (10.307.104, Alfredo Serrano Masip, p. 80144 = c3p1),
    cand. 3 INICIATIVA PER CATALUNYA VERDS - ESQUERRA UNIDA I ALTERNATIVA
    (ICV-EUiA), SUPLENTES #1: "Sra. Soledat Guasch Duran" -> "Sra. Soledat Gasch
    Duran". OJO: la errata cita "…(ICV - EUIA)" (espacios y mayúsculas) pero el
    archivo imprime "(ICV-EUIA)"; se ancla únicamente la línea de nombre, única
    en el corpus (x1 en 80144). El nº ("1 ") va en línea separada (formato 2010).
    """
    # Regex expanded into two fast string replacements
    text = text.replace("Sra. Soledat Guasch Duran", "Sra. Soledat Gasch Duran")
    text = text.replace("Sra. Soledat guasch Duran", "Sra. Soledat Gasch Duran")
    return text


CATALUNA_2024_05_REPLACEMENTS = {
    "Candidatura núm. 3\nESQUERRA REPUBLICANA DE CATALUNYA (ERC / ESQUERRA)": "Candidatura núm. 3\nESQUERRA REPUBLICANA DE CATALUNYA (ERC)",
    "Candidatura num. 3\nESQUERRA REPUBLICANA DE CATALUNYA (ERC / ESQUERRA)": "Candidatura núm. 3\nESQUERRA REPUBLICANA DE CATALUNYA (ERC)",
}
P_CATALUNA_2024_05_LITERALS = re.compile(
    "|".join(map(re.escape, CATALUNA_2024_05_REPLACEMENTS.keys()))
)


@register_fixer("cataluna", 2024, 5)
def fix_cataluna_2024_05(text: str) -> str:
    """Corrige el DOGC núm. 9143 (15/16.4.2024, candidaturas al Parlamento de
    Catalunya 2024) via el DOGC núm. 9145 (18.4.2024, "Edicto de 16 de abril de
    2024, por el que se hace pública la corrección de una errata en el Edicto
    de 15 de abril de 2024, de la Junta Electoral Provincial de Barcelona,
    DOGC núm. 9143, pág. 7 de 46").

    Errata única. BARCELONA (24.107.081, Jaime Juan Álvarez Álvarez), c1 p6
    (pág. 7 de 46), CANDIDATURA 3 ERC: la línea de formación lleva
    "ESQUERRA REPUBLICANA DE CATALUNYA (ERC / ESQUERRA)" y debe decir
    "ESQUERRA REPUBLICANA DE CATALUNYA (ERC)" (se omite la parte "ESQUERRA").
    OJO: la misma línea "(ERC / ESQUERRA)" también aparece en el edicto de
    GIRONA (c2 p3, CANDIDATURA 4). Se ancla el bloque de 2 líneas
    "Candidatura núm. 3\\nESQUERRA REPUBLICANA DE CATALUNYA (ERC / ESQUERRA)"
    (c1 p6); en Girona el cand. es num. 4, así que el ancla no collide.
    """
    return P_CATALUNA_2024_05_LITERALS.sub(
        lambda m: CATALUNA_2024_05_REPLACEMENTS[m.group(0)], text
    )
