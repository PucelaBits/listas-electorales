import re

from ._common import register_fixer


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


# BOC 88, err_1 (Junta Electoral de Santa Cruz de Tenerife, BOC nº 82 de 30.4.19):
#   La Palma, cand. n.º 5 COALICIÓN CANARIA (CCa) was proclaimed with the wrong
#   denomination; it should be COALICIÓN CANARIA-PARTIDO NACIONALISTA CANARIO
#   (CCa-PNC). Only err_1 belongs to the 2019 batch (the folder's
#   candidaturas*.pdf are the 2019 proclamations); err_2/err_3 in this folder
#   are 2023 corrections for the 2023 batch and target INSULAR
#   circunscripciones that have no candidaturas file in the repo, so they are
#   NOT POSSIBLE here (flagged for individual review).
@register_fixer("canarias", 2019, 5)
def fix_canarias_2019_05(text: str) -> str:
    text = text.replace(
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA (CCa)",
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA-PARTIDO NACIONALISTA CANARIO (CCa-PNC)",
    )
    return text


# BOC 85, err_1 (Junta Electoral de Canarias, n.1350, BOC n.84 de 2.5.2023):
#   Circunscripción autonómica, cand. n.º 11 AHORA TÚ (AT): "Antonio Orlando
#   Camacho Betencor" -> "... Betancor".
#   This file's candidate-list body is drawn in a custom-encoded font whose
#   glyphs come back as PUA characters U+F0xx (i.e. the byte value + 0xF000),
#   so the pattern is written with those codepoints; the sequence is unique in
#   the document (1 occurrence). err_2/err_3 in the 2019 folder correct 2023
#   INSULAR circunscripciones, which are not present in this file (autonómica
#   only), so they cannot be applied here.
@register_fixer("canarias", 2023, 5)
def fix_canarias_2023_05(text: str) -> str:
    # CAMACHO BETENCOR  ->  CAMACHO BETANCOR.
    # Body glyphs are PUA (U+F0xx == 0x00xx); \u escapes build those literals.
    #   CAMACHO + ' ' = F043 F041 F04D F041 F043 F048 F04F F020
    #   BETENCOR       = F042 F045 F054 F045 F04E F043 F04F F052
    #   (corrected) BETANCOR = F042 F045 F054 F041 F04E F043 F04F F052
    text = text.replace(
        "\uf043\uf041\uf04d\uf041\uf043\uf048\uf04f\uf020\uf042\uf045\uf054\uf045\uf04e\uf043\uf04f\uf052",
        "\uf043\uf041\uf04d\uf041\uf043\uf048\uf04f\uf020\uf042\uf045\uf054\uf041\uf04e\uf043\uf04f\uf052",
    )
    return text
