import re

from ._common import register_fixer

CEUTA_2015_05_REPLACEMENTS = {
    "16. Don PATRICIA DIAZ MATEO": "16. Doña PATRICIA DIAZ MATEO",
    "20. Don LIDIA GALAN": "20. Doña LIDIA GALAN",
    "3. Don HOSAIN EL HADDAD ALÍ": "3. Doña HAMAMA BENAASSATI ABDESELAM",
    "3. Don HOSAIN EL HADDAD ALí": "3. Doña HAMAMA BENAASSATI ABDESELAM",
}
P_CEUTA_2015_05_LITERALS = re.compile(
    "|".join(map(re.escape, CEUTA_2015_05_REPLACEMENTS.keys()))
)


@register_fixer("ceuta", 2015, 5)
def fix_ceuta_2015_05(text: str) -> str:
    """Corrige el B.O.C.C.E. Extraordinario núm. 6 (28.4.2015, anuncio nº 10,
    "Proclamación de las candidaturas… Elecciones Locales y Autonómicas, 24 de
    mayo") via el B.O.C.C.E. Extraordinario núm. 7 (28.4.2015), que por el
    art. 105.2 Ley 30/1992 publica el "texto íntegro" del anuncio anulando el
    anterior (secretaria: Carmen Rodriguez Vozmediano, Junta Electoral de Zona
    de Ceuta).

    El "texto íntegro" solo se diferencia del original en 3 líneas (diff
    página a página de ambos PDF: 308 nombres a y b, idem). Se aplican solo
    esos tres deltas:
      - Candidatura 3. LOS VERDES-GRUPO VERDE, nº 16: "Don" -> "Doña"
        (PATRICIA DIAZ MATEO, p. 146).
      - Candidatura 3, nº 20: "Don" -> "Doña" (LIDIA GALAN ORTIZ, p. 146).
      - Candidatura 5. PARTIDO DEMOCRATICO Y SOCIAL DE CEUTA (P.D.S.C.), nº 3:
        nombre completo "Don HOSAIN EL HADDAD ALÍ" -> "Doña HAMAMA BENAASSATI
        ABDESELAM" (p. 148). Hay OTRO "19. Don HOSAIN EL HADDAD ALÍ" (otra
        candidatura) que la errata NO toca; el ancla "^3\\." lo descarta.
    """
    return P_CEUTA_2015_05_LITERALS.sub(
        lambda m: CEUTA_2015_05_REPLACEMENTS[m.group(0)], text
    )
