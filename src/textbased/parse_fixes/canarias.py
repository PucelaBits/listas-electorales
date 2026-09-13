import re

from common import NAME_WHITELIST_CHARS, NAME_WHITELIST_CHARS_UPPER

from ._common import number_candidates, register_fixer


def _canarias_province_fix(text: str) -> str:
    suffix = 1
    text = text.replace("Fuerteventura", f"CAN-{suffix}")
    text = text.replace("FUERTEVENTURA", f"CAN-{suffix}")
    text = text.replace("Gran Canaria", f"CAN-{suffix + 1}")
    text = text.replace("GRAN CANARIA", f"CAN-{suffix + 1}")
    text = text.replace("La Gomera", f"CAN-{suffix + 2}")
    text = text.replace("LA GOMERA", f"CAN-{suffix + 2}")
    text = text.replace("Lanzarote", f"CAN-{suffix + 3}")
    text = text.replace("LANZAROTE", f"CAN-{suffix + 3}")
    text = text.replace("La Palma", f"CAN-{suffix + 4}")
    text = text.replace("LA PALMA", f"CAN-{suffix + 4}")
    text = text.replace("Tenerife", f"CAN-{suffix + 5}")
    text = text.replace("TENERIFE", f"CAN-{suffix + 5}")
    text = text.replace("El Hierro", f"CAN-{suffix + 6}")
    text = text.replace("EL HIERRO", f"CAN-{suffix + 6}")
    return text


# BOC 88 (err_1) y BOC 91 (err_2), err.pdf.
# err_1 (Junta Electoral de Santa Cruz, La Palma): candidate nº1 of
#   INICIATIVAPOR LAPALMA-NUEVACANARIAS (NCa) lacks the "Independiente" label.
# err_2 (Junta Electoral de Las Palmas, Lanzarote PIL-CCN cand. 7):
#   cand. 8 "Pedro Jesús Betancor Machón" -> "Machín"; supl. 1 "Briton" -> "Brito".
# err_2 (Santa Cruz, La Palma PSOE): candidate 5 "Félix Andrés Gonzalo Lorenzo" -> "González Lorenzo".
# The Lanzarote names appear in both candidaturas_1.pdf and candidaturas_2.pdf
# (duplicated publication of the same proclamation); the global substitution
# fixes both copies.
@register_fixer("canarias", 2007, 5)
def fix_canarias_2007_05(text: str) -> str:
    text = text.replace(
        "D. Juan Carlos Navarro Pérez",
        "D. Juan Carlos Navarro Pérez (Independiente)",
    )
    text = text.replace("Pedro Jesús Betancor Machón", "Pedro Jesús Betancor Machín")
    text = text.replace("Germán Briton Martín", "Germán Brito Martín")
    text = text.replace("Félix Andrés Gonzalo Lorenzo", "Félix Andrés González Lorenzo")
    return text


# BOC 84 (err_1), BOC 83 (err_2), BOC 88 (err_3), err.pdf.
# err_1 (Junta Las Palmas): Fuerteventura CC-PNC-CCN supl. 2 "Venancio" ->
#   "Venancia"; Gran Canaria PUM+J cand. 7 "Noela" -> "Noelia"; and the
#   abbreviation printed as "Nca" instead of "NCa" (4 headings in
#   candidaturas_1.pdf).
# err_2 (Junta Santa Cruz): La Palma PSOE cand. 6 "Feliz" -> "Félix" (columns
#   in candidaturas_2.pdf: the name is split across lines); CSDC Tenerife
#   cand. 1 "Rosa Rivero Abreu" -> "Rosi Rivero Abreu"; NCa (cand. 10)
#   Tenerife denomination "NUEVA CANARIAS" -> "SOCIALISTAS POR TENERIFE-LOS
#   VERDES DE CANARIAS-NUEVA CANARIA" and cand. 2 "Méndez Lloret" ->
#   "Llorens".
# err_3 (Junta Santa Cruz): PUM+J (cand. 16) Tenerife cand. 8 "Iglesias Sangil"
#   -> "San Gil"; cand. 9 "Anotomía Mª Vera" -> "Antonia Mª Vera".
P_CANARIAS_2011_05 = re.compile(r"^NUEVA CANARIAS ?\nNCa", flags=re.MULTILINE)


@register_fixer("canarias", 2011, 5)
def fix_canarias_2011_05(text: str) -> str:
    # err_1
    text = text.replace(
        "Doña Venancio Pérez Hernández", "Doña Venancia Pérez Hernández"
    )
    text = text.replace("7 Doña Noela García Ramos", "7 Doña Noelia García Ramos")
    text = text.replace("Siglas: Nca", "Siglas: NCa")
    # err_2
    # (cand_2.pdf prints multi-column: each name token on its own line with
    #  trailing spaces; match the block exactly and only change the token
    #  the erratum corrects.)
    text = text.replace(
        "6 Don \nFeliz Andrés \nGonzález \nLorenzo",
        "6 Don \nFélix Andrés \nGonzález \nLorenzo",
    )
    text = text.replace(
        "1 Doña\nRosa\nRivero\nAbreu",
        "1 Doña\nRosi\nRivero\nAbreu",
    )
    # The long denomination only appears as an exact line followed by the
    # "NCa" siglas line; the La Gomera heading " NUEVA CANARIAS" (leading
    # space, cand. 2) must be left untouched (it is not in the errata).
    text = P_CANARIAS_2011_05.sub(
        "SOCIALISTAS POR TENERIFE-LOS VERDES DE CANARIAS-NUEVA CANARIA\nNCa",
        text,
    )
    text = text.replace(
        "Arturo Mario\nMéndez\nLloret",
        "Arturo Mario\nMéndez\nLlorens",
    )
    # err_3
    text = text.replace("Iglesias\nSangil", "Iglesias\nSan Gil")
    text = text.replace(
        "Anotomía Mª\nVera\nPerera",
        "Antonia Mª\nVera\nPerera",
    )
    return text


# BOC 82, err.pdf (Junta Electoral de Las Palmas, BOC nº 80 de 28.4.15):
#   Lanzarote, Candidatura núm.: 10 UNIDOS.
#   cand. 2 "Francisco Guzman Rodriguez" -> "... Reyes" (missing second surname);
#   cand. 4 "Natalia Curbelo Cabrero" -> "... Cabrera".
#   Names are printed uppercase; both full strings are unique in the file.
@register_fixer("canarias", 2015, 5)
def fix_canarias_2015_05(text: str) -> str:
    text = text.replace(
        "FRANCISCO GUZMAN RODRIGUEZ",
        "FRANCISCO GUZMAN RODRIGUEZ REYES",
    )
    text = text.replace(
        "NATALIA CURBELO CABRERO",
        "NATALIA CURBELO CABRERA",
    )
    return text


_CANARIAS_2019_05_LAST_NUMBER = None
_CANARIAS_2019_05_CANDIDATE_REGEX = re.compile(
    r"^(?!NO PROCLAMADA)(?:["
    + NAME_WHITELIST_CHARS_UPPER
    + r"\.]+ +)+(?:\(["
    + NAME_WHITELIST_CHARS_UPPER
    + r"\. ]+\) +)?(?:["
    + NAME_WHITELIST_CHARS_UPPER
    + r"\.]+ *)+(?:\(["
    + NAME_WHITELIST_CHARS
    + r"\. ]+\))? *$"
)


@register_fixer("canarias", 2019, 5)
def fix_canarias_2019_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA (CCa)",
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA-PARTIDO NACIONALISTA CANARIO (CCa-PNC)",
    )
    # Facilitate parsing
    text = text.replace(
        "AHORA CANARIAS ALTERNATIVA NACIONALISTA CANARIA (ANC) Y UNIDAD\n",
        "AHORA CANARIAS ALTERNATIVA NACIONALISTA CANARIA (ANC) Y UNIDAD ",
    )
    text = text.replace(
        "AHORA CANARIAS ALTERNATIVA NACIONALISTA CANARIA ANC y UNIDAD\n",
        "AHORA CANARIAS ALTERNATIVA NACIONALISTA CANARIA ANC y UNIDAD ",
    )
    text = text.replace("(PODEMOS\n", "(PODEMOS)\n")
    text = text.replace("Mª.", "MARÍA")
    # Fix missing numbers
    global _CANARIAS_2019_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        _CANARIAS_2019_05_CANDIDATE_REGEX,
        last_number=_CANARIAS_2019_05_LAST_NUMBER,
    )
    _CANARIAS_2019_05_LAST_NUMBER = last_number
    text = _canarias_province_fix(text)
    return text


_CANARIAS_2023_05_LAST_NUMBER = None
_CANARIAS_2023_05_CANDIDATE_REGEX = re.compile(
    r"^(?!NO PROCLAMADA)(?:["
    + NAME_WHITELIST_CHARS_UPPER
    + r"]+ +)+(?:\(["
    + NAME_WHITELIST_CHARS_UPPER
    + r" ]+\) +)?(?:["
    + NAME_WHITELIST_CHARS_UPPER
    + r"]+ *)+(?:\(["
    + NAME_WHITELIST_CHARS
    + r" ]+\))? *$"
)


@register_fixer("canarias", 2023, 5)
def fix_canarias_2023_05(text: str) -> str:
    # TODO: err.pdf
    # Remove weird duplication
    if "MATÍAS HERNÁNDEZ PADRÓN" in text:
        text = text.replace(
            "KEVIN TOMÁS QUEVEDO MARTÍN \n \nCandidatura núm.: 10. CONTIGO SOMOS DEMOCRACIA (CONTIGO) \n \nNO PROCLAMADA \n \nCandidatura núm.: 11. AHORA TÚ (AT) \n",
            "",
        )
    elif "ANTONIO MARÍN MUÑOZ" in text:
        text = text.replace(
            "\nSAÚL GÓMEZ ALBEROLA \nNAIRA MARRERO JAÉN \n \nSuplentes \nALEXANDER VELÁZQUEZ DÍAZ \nMARÍA DEL CARMEN LLANOS GAVIRIA \nRAMÓN TRUJILLO MORALES \n \nCandidatura núm.: 14. PAIS CON GESTORES (PAIS CON GESTORES) \n",
            "",
        )
    # Fix missing numbers
    global _CANARIAS_2023_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        _CANARIAS_2023_05_CANDIDATE_REGEX,
        last_number=_CANARIAS_2023_05_LAST_NUMBER,
    )
    _CANARIAS_2023_05_LAST_NUMBER = last_number

    return text
