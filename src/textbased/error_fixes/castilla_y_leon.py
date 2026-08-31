import re

from ._common import register_fixer

P_CYL_1983_05 = re.compile(r"^COALICION PCOE-PCEU", flags=re.MULTILINE)


@register_fixer("castilla_y_leon", 1983, 5)
def fix_castilla_y_leon_1983_05(text: str) -> str:
    return P_CYL_1983_05.sub("3. COALICION PCOE-PCEU", text)


# Boletín Oficial de Castilla y León n.º 86 (08-05-1991), "Corrección de
# errores a las Candidaturas proclamadas ... convocadas por Decreto 60/1991,
# de 1 de abril", que rectifican la publicación de B.O.C.yL. n.º 81 (30-abr).
# 31 rectificaciones repartidas por provincia; se aplica solo la que el
# archivo candidaturas.pdf contiene. Las líneas de candidatos del archivo
# llevan punto final y acentos irregulares; cada patrón se ancla al número de
# candidato y se verifica que sea UNIFICADO en todo el documento antes de
# sustituir. Los dos casos ambigüos (Burgos "8.- Los Verdes" y Soria
# "2.- Coalición Izquierda Unida", que se repiten en otra provincia) se
# desambiguan anclando también la línea del candidato 1 de esa candidatura.
# Se OMITEN (no expresables como find/replace, requieren revisión manual):
#   - Zamora, cand. 2 (P.S.O.E.): el erratum dice que "se ha incluido
#     «Partido Socialista de Castilla y León (P.S.C.L.)»" que "no consta en el
#     edicto" -> es una corrección del ENUNCIADO/cabecera (no de un nombre),
#     y la cabecera del archivo dice "...Obrero Español (P.S.C.L-P.S.O.E.)",
#     de modo que no hay un único string que sustituir.
#   - err_2.pdf (B.O.C.yL. n.º 92, 16-05-1991): "debe incluirse el siguiente
#     titular:" (una INSERCIÓN de un titular antes del párrafo del P.P.) que
#     aplica sobre el propio err_1, no sobre candidaturas.pdf; no hay texto a
#     sustituir en el archivo.
# (castilla_y_leon usa el prefijo "cyl")
CASTILLA_Y_LEON_1991_05_REPLACEMENTS = {
    "5. Maria Cruz Rodriguez Saldaña.": "5. M.ª Cruz Rodríguez Saldaña.",
    "8.- Los Verdes (L.V.)\n1. Raquel Plasencia Diez.": "8.- Partido Político Los Verdes (L.V.)\n1. Raquel Plasencia Diez.",
    "2. José María Arribas Moral.": "2. José M.ª Arribas Moral.",
    "10.- Centro Democrático y Social (C.D.S.)": "10.- Partido Centro Democrático y Social (C.D.S.)",
    "9. Benito de la torre Vega.": "9. Benito de la Torre Vega.",
    "3. Dolores Otero Rodríguez de las Heras.": "3. M.ª Dolores Otero Rodríguez de las Heras.",
    "10. Fernando Arvizu y Galarraga.": "10. Fernando de Arvizu y Galarraga.",
    "15. Natividad Cordero Monrroy.": "15. Natividad Cordero Monroy.",
    "10. Maria-Montserrat Alvarez Velasco.": "10. María Monserrat Alvarez Velasco.",
    "15. Maria Inmaculada Fuente Villaba.": "15. María Inmaculada Fuente Villalba.",
    "5. Antonio de San Mateo Gil.": "5. Antonio de Sanmateo Gil.",
    "12. Maria Teresa González Alonso.": "12. Teresa González Alonso.",
    "5. Maria Luisa Gavela Ordoñez.": "5. María Luisa Gabela Ordóñez.",
    "9. Heliberto López López.": "9. Eliberto López López.",
    "1. Carmen Elena Varges López.": "1. Carmen Elena Vargues López.",
    "3. Eliseo Garcia Guitiérrez.": "3.Eliseo García Gutiérrez.",
    "2.- Partido Politico los Verdes (P.V.)": "2.- Partido Politico los Verdes (L.V.)",
    "4. Jacinda Lorenzo Pascua.": "4. Jacinta Lorenzo Pascua.",
    "9. Luis Enriquez Espinoza Cuerra.": "9. Luis Enrique Espinoza Guerra.",
    "1. Miguel Angel de Diego Nuñez.": "1. Miguel Ángel Diego Núñez.",
    "5. Pedro Carlos Acevedo y González.": "5. Pedro Carlos Acevedo González.",
    "7. Rafael Vargas Ribera.": "7. Rafael Vargas Rivera.",
    "9. Rafael de Diego Nuñez.": "9. Rafael Diego Núñez.",
    "2. Maria del Carmen Garcia Rosado y Garcia.": "2. María del Carmen García Rosado García.",
    "9. Luis Filguerina Canal.": "9. Luis Filgueira Canal.",
    "3. Beatriz Saa y de Corral.": "3. Beatriz de Saa Corral.",
    "3.- Unión Castellana (U.C.)": "3.- Unión Castellanista (U.C.)",
    "2.- Coalición Izquierda Unida (I.U.)\n1. Alejandro Abad Gil.": "2.- Izquierda Unidad (I.U.)\n1. Alejandro Abad Gil.",
    "1. José Oliver Alvarez Seco.": "1. José Olivier Álvarez Seco.",
    "4. Maria Isabel Blanca T. Fernández Marassa.": "4. M.ª Isabel Blanca T. Fernández Marassa.",
    "6. Javier del Riego Celada.": "6. Javier Riego Celada.",
}
P_CYL_1991_05_LITERALS = re.compile(
    "|".join(map(re.escape, CASTILLA_Y_LEON_1991_05_REPLACEMENTS.keys()))
)


@register_fixer("castilla_y_leon", 1991, 5)
def fix_castilla_y_leon_1991_05(text: str) -> str:
    return P_CYL_1991_05_LITERALS.sub(
        lambda m: CASTILLA_Y_LEON_1991_05_REPLACEMENTS[m.group(0)], text
    )


# Boletín Oficial de Castilla y León n.º 98 (25-05-1999), "Corrección de errores
# a las candidatura(s) proclamadas ... Cortes de Castilla y León, convocadas por
# Decreto 66/1999 de 19-04-1999", que rectifica la publicación de B.O.C.yL.
# n.º 93 (18-05-1999). 11 rectificaciones:
#   PALENCIA: la cand. 3 "IZQUIERDA UNIDA DE CASTILLA Y LEÓN" lleva la sigla
#     "(I.U.-CL)" y debe ser "(IU-CyL)". El error está solo en el paréntesis,
#     y el token "(I.U.-CL)" es único en todo el documento (el archivo la
#     escribe como "LEÓN", aunque el erratum lo escribe "LEON"); por eso
#     basta con sustituir el paréntesis y no el nombre del partido.
#   ZAMORA: el erratum expande la abreviatura "Mª" en cada nombre ("D. M.ª X" ->
#     "D. María X") y corrige un apellido ("Allosa" -> "Alloza"). El erratum usa
#     "Dª" para las mujeres; en el archivo se conserva lo que hay.
#   NOTA: no se toca la cabecera "1.– IZQUIERDA UNIDA DE CASTILLA Y LEON (IU)"
#     de Zamora, porque el erratum solo cita los nombres de candidatos de esa
#     candidatura y no su sigla.  El "–" es un guion de interlínea y el "ª" el
#     ordinal de título, ambos literal en el archivo.
# (castilla_y_leon usa el prefijo "cyl")
CASTILLA_Y_LEON_1999_06_REPLACEMENTS = {
    "(I.U.-CL)": "(IU-CyL)",
    "1. D. Gabriel Guijosa Allosa.": "1. D. Gabriel Guijosa Alloza.",
    "2. Dª Mª del Carmen Luis Heras.": "2. Dª María del Carmen Luis Heras.",
    "3. Dª Mª Teresa García López.": "3. Dª María Teresa García López.",
    "5. Dª Mª Elena García Rodríguez.": "5. Dª María Elena García Rodríguez.",
    "3. Dª Mª Isabel Blanca Teresa Fernández Marassa.": "3. Dª María Isabel Blanca Teresa Fernández Marassa.",
    "6. Dª Mª Inmaculada García Rioja.": "6. Dª María Inmaculada García Rioja.",
    "7. Dª Mª Isabel Perero Llamas.": "7. Dª María Isabel Perero Llamas.",
    "7. Dª Mª Begoña Mateos Lorenzo.": "7. Dª María Begoña Mateos Lorenzo.",
    "8. Dª Mª Teresa Regueras Bermejo.": "8. Dª María Teresa Regueras Bermejo.",
    "3. Dª Mª Jesús Piorno Hernández.": "3. Dª María Jesús Piorno Hernández.",
    "2. Dª Mª Julia Arias Rodríguez.": "2. Dª María Julia Arias Rodríguez.",
    "3. Dª Mª Luisa Arias Maneiro.": "3. Dª María Luisa Arias Maneiro.",
    "1. Dª Mª Teresa Rubio Herrero.": "1. Dª María Teresa Rubio Herrero.",
    "4. Dª Mª del Carmen Campos Pérez.": "4. Dª María del Carmen Campos Pérez.",
    "1. Dª Mª del Pilar Calvo Fernández.": "1. Dª María del Pilar Calvo Fernández.",
    "2. Dª Mª Elisa del Pino Mañanes.": "2. Dª María Elisa del Pino Mañanes.",
    "5. Dª Mª del Carmen Barrio Sánchez.": "5. Dª María del Carmen Barrio Sánchez.",
    "8. Dª Mª Mercedes Corral Velasco.": "8. Dª María Mercedes Corral Velasco.",
}
P_CYL_1999_06_LITERALS = re.compile(
    "|".join(map(re.escape, CASTILLA_Y_LEON_1999_06_REPLACEMENTS.keys()))
)


@register_fixer("castilla_y_leon", 1999, 6)
def fix_castilla_y_leon_1999_06(text: str) -> str:
    return P_CYL_1999_06_LITERALS.sub(
        lambda m: CASTILLA_Y_LEON_1999_06_REPLACEMENTS[m.group(0)], text
    )


@register_fixer("castilla_y_leon", 2003, 5)
def fix_castilla_y_leon_2003_05(text: str) -> str:
    """Aplica las erratas del BOC n.º 88 (12-mayo-2003) que corrige el
    Suplemento al BOC n.º 80 (29-abril-2003) — Decreto 1/2003, de 31 de marzo,
    del Presidente de la Junta de Castilla y León.

    La errata (JEP BURGOS) deja sin efecto la proclamación de la candidatura
    de Izquierda Unida de Castilla y León de 28-abril-2003 y la vuelve a
    proclamar, en ejecución de la sentencia del Tribunal Constitucional en el
    recurso de amparo n.º 2.602/03. Comparando la lista reproclamada con la
    publicada, solo difieren dos cosas (el resto de nombres y suplentes son
    idénticos):
      1. Los dos primeros candidatos estaban intercambiados: el archivo dice
         "1.º CASTO GARCÍA GONZÁLEZ / 2.º LUIS CASTRO BERROJO" pero debe ser
         "1.º LUIS GARCÍA SANZ / 2.º CASTO GARCÍA GONZÁLEZ". Se sustituye el
         bloque de dos líneas (único en todo el documento) por el orden
         correcto.
      2. "Dª MIREN JAIONE AVILA ESTEFANÍA" debe ser "…AVILA… con tilde:
         ÁVILA" — "Jaione Ávila Estefanía" (único en el documento).
    Nota: la errata escribe los nombres en el estilo propio del BOC 88
    ("D.ª", finales con punto); se conserva el estilo del propio archivo
    ("Dª", sin punto final) y solo se corrigieron las dos diferencias
    sustantivas. El resto de candidaturas IU-CyL de otras provincias (p. e.
    LEÓN p.2/3, SALAMANCA p.6, SEGOVIA p.8, SORIA p.9, ZAMORA p.11) son
    distintas y quedan intactas.
    """
    text = text.replace(
        "D. CASTO GARCÍA GONZÁLEZ\nD. LUIS CASTRO BERROJO",
        "D. LUIS GARCÍA SANZ\nD. CASTO GARCÍA GONZÁLEZ",
    )
    text = text.replace(
        "Dª MIREN JAIONE AVILA ESTEFANÍA",
        "Dª MIREN JAIONE ÁVILA ESTEFANÍA",
    )
    return text


@register_fixer("castilla_y_leon", 2011, 5)
def fix_castilla_y_leon_2011_05(text: str) -> str:
    """Aplica las erratas del BOC n.º 80 (27-abril-2011) que corrige el BOC
    n.º 79 (26-abril-2011) — Decreto 1/2011, de 28 de marzo.

    OJO: este candidaturas.pdf tiene la capa de texto PARCIALMENTE garbada por
    codificación de fuente: los spans de ArialMT son limpios, pero varios
    titulares (Arial-BoldMT subconjunto) salen con un cifrado César por fuente
    y los DÍGITOS mapeados a caracteres de control (p. ej. "8.- IZQUIERDA..."
    aparece como bytes \x18\x11\x10...). Esto limita lo que puede hacerse con
    un find/replace: SOLO pueden corregirse las líneas cuyo texto sale limpio.

    Aplicadas (todas en spans ArialMT limpios, únicas en el documento):
      1. SALAMANCA (p. 32052): "Doña JOSEFA GARCÍA CIRAC" -> "Doña Mª JOSEFA
         GARCÍA CIRAC" (cand. 1 PP).
      2. SALAMANCA (p. 32054): suplente de Verdes de Salamanca: "Suplentes:\n1.\nDon EMILIO SANZ AIRAS"
         -> "Suplentes:\n2.\nDon EMILIO SANTOS AIRAS" (bloqueo de 3 líneas para
         anclar el número "1." que va en línea propia).
      3. SALAMANCA (p. 32058, PREPAL): "Doña FRANCISCO GARCIA MARTIN" ->
         "Don FRANCISCO GARCIA MARTIN" (solo cambia el honorífico
         Doña->Don; se conserva el estilo sans-acentos del "debe decir").
      4. SALAMANCA (p. 32058, PREPAL): "11. Don MARIA DEL CARMEN COSCARON VILLAR"
         -> "11. Doña MARIA DEL CARMEN COSCARON VILLAR" (honorífico Don->Doña).
      5. SEGOVIA (p. 32060, PSOE): "Don ALBERTO SERRA BARRERO (PSOE)" ->
         "Don ALBERTO SERNA BARRERO (PSOE)".
      6. SORIA (p. 32064, UCE): "Doña ROSA MARIA TERESA DEL CARMEN
         CARAMANZANA ARAUJO " -> "Doña ROSA MARÍA TERESA DEL CARMEN
         CARAMAZANA ARAUJO " (conserva el espacio final del archivo).

    NO POSIBLE (titulares en la capa garbada — no se pueden reproducir los
    strings limpios de "debe decir" sobre el texto garbado; ver
    /memories/repo/error_fixes_regex.md, taxonomía de garbled):
      - SALAMANCA (p. 32053): "4.- FORMACIÓN POLÍTICA: VERDES DE SALAMANCA
        (9(5'(6)" [garbled] debería ir a "4. VERDES DE SALAMANCA (VERDES)".
      - SEGOVIA (p. 32060): "4.- SEGOVIA DE IZQUIERDAS" [garbled] debe añadir
        "(SEGOVIA DE IZQUIERDAS)" al final.
      - SORIA (p. 32064): "8.- UNIFICACIÓN COMUNISTA DE ESPAÑA (UCE)" [garbled:
        "817$..." -> con acento en la A de UNIFICACIÓN].
    """
    text = text.replace("Doña JOSEFA GARCÍA CIRAC", "Doña Mª JOSEFA GARCÍA CIRAC")
    # El número del suplente "1." va en línea propia; se ancla a las
    # 3 líneas para que sea único (hay muchos "1." aislados).
    text = text.replace(
        "Suplentes:\n1.\nDon EMILIO SANZ AIRAS",
        "Suplentes:\n2.\nDon EMILIO SANTOS AIRAS",
    )
    text = text.replace("Doña FRANCISCO GARCIA MARTIN", "Don FRANCISCO GARCIA MARTIN")
    text = text.replace(
        "11. Don MARIA DEL CARMEN COSCARON VILLAR",
        "11. Doña MARIA DEL CARMEN COSCARON VILLAR",
    )
    text = text.replace(
        "Don ALBERTO SERRA BARRERO (PSOE)",
        "Don ALBERTO SERNA BARRERO (PSOE)",
    )
    text = text.replace(
        "Doña ROSA MARIA TERESA DEL CARMEN CARAMANZANA ARAUJO ",
        "Doña ROSA MARÍA TERESA DEL CARMEN CARAMAZANA ARAUJO ",
    )
    return text


@register_fixer("castilla_y_leon", 2026, 3)
def fix_castilla_y_leon_2026_03(text: str) -> str:
    """Aplica las dos correcciones de errores (err_1 = BOC n.º 34, 19-feb-2026,
    y err_2 = BOC n.º 35, 20-feb-2026) del texto de candidaturas publicado en
    el BOC n.º 32 (17-feb-2026) — Decreto 1/2026, de 19 de enero.

    Candidaturas.pdf es el BOC 32 completo; la capa de texto es limpia.
    Corrigen: PALENCIA (cand. 3 y 7 "España Vaciada"/VOX, cand. 10
    Mundo+Justo, cand. 14 SALF), LEÓN (cand. 16 SALF) y VALLADOLID (cand. 7
    PACMA). Todas las líneas diana son únicas en el documento.

      1. PALENCIA: "Candidatura núm.: 3. ESPAÑA VACIADA (ESPAÑA VACIADA)"
         -> "…(EV)" (el acrónimo repetía el nombre).
      2. PALENCIA VOX: "4.\t Doña MARÍA DEL PILAR JUNCO NAVASCUES"
         -> "…NAVASCUÉS" (acentos).
      3. PALENCIA Mundo+Justo: "2.\t Don AMADOR PARIS CAMINERO"
         -> "…PARÍS CAMINERO".
      4. PALENCIA SALF: "4.\t Doña NOEMI DORADO MARTINEZ"
         -> "4.\t Doña NOEMÍ DORADO MARTÍNEZ".
      5. LEÓN SALF: "12.\tDoña ALISSON PLET TEJADA HERRERA"
         -> "12.\tDoña ALISSON POLET TEJADA HERRERA".
      6. VALLADOLID PACMA: "Candidatura núm.: 7. PARTIDO ANIMALISTA CONTRA EL
         MALTRATO ANIMAL \n(PACMA)" -> "…PARTIDO ANIMALISTA CON EL MEDIO AMBIENTE
         \n(PACMA)". Se conserva el bloque de dos líneas (nombre con espacio
         final + "(PACMA)" en su propia línea, como en el archivo) y el
         "(PACMA)" — el "debe decir" de la errata se corta antes del
         acrónimo pero lo que cambia es el nombre. (Nota: en este BOC 32 el
         resto de candidaturas PACMA ya figuran como "…CON EL MEDIO AMBIENTE
         (PACMA)"; la de Valladolid era la única con el nombre anterior.)
    Se preservan exactamente los separadores del archivo (tabulación: "4.\t "
    con espacio vs. "12.\t" sin espacio) y los espacios finales.

    Las "Páginas" de la errata (36, 38, 40, 41, 43, 68) son las del BOC 32
    impreso; al offset +11 sobre el índice de página del PDF (36→p25,
    38→p27, 40→p29, 41→p30, 43→p32, 68→p57).
    """
    text = text.replace(
        "Candidatura núm.: 3. ESPAÑA VACIADA (ESPAÑA VACIADA)",
        "Candidatura núm.: 3. ESPAÑA VACIADA (EV)",
    )
    text = text.replace(
        "4.\t Doña MARÍA DEL PILAR JUNCO NAVASCUES",
        "4.\t Doña MARÍA DEL PILAR JUNCO NAVASCUÉS",
    )
    text = text.replace(
        "2.\t Don AMADOR PARIS CAMINERO",
        "2.\t Don AMADOR PARÍS CAMINERO",
    )
    text = text.replace(
        "4.\t Doña NOEMI DORADO MARTINEZ",
        "4.\t Doña NOEMÍ DORADO MARTÍNEZ",
    )
    text = text.replace(
        "12.\tDoña ALISSON PLET TEJADA HERRERA",
        "12.\tDoña ALISSON POLET TEJADA HERRERA",
    )
    text = text.replace(
        "Candidatura núm.: 7. PARTIDO ANIMALISTA CONTRA EL MALTRATO ANIMAL \n(PACMA)",
        "Candidatura núm.: 7. PARTIDO ANIMALISTA CON EL MEDIO AMBIENTE \n(PACMA)",
    )
    return text
