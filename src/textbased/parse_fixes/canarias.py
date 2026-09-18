import re

from ._common import (
    LOWER_DON_CANDIDATE_NAME_REGEX,
    UPPER_CANDIDATE_REGEX,
    fix_maria_ocr,
    fix_multiline_candidacy_naming,
    number_candidates,
    register_fixer,
)


def _canarias_province_fix(text: str) -> str:
    suffix = 1
    text = text.replace("Fuerteventura\n", f"CAN-{suffix}\n")
    text = text.replace("FUERTEVENTURA\n", f"CAN-{suffix}\n")
    text = text.replace("Gran Canaria\n", f"CAN-{suffix + 1}\n")
    text = text.replace("GRAN CANARIA\n", f"CAN-{suffix + 1}\n")
    text = text.replace("La Gomera\n", f"CAN-{suffix + 2}\n")
    text = text.replace("LA GOMERA\n", f"CAN-{suffix + 2}\n")
    text = text.replace("Lanzarote\n", f"CAN-{suffix + 3}\n")
    text = text.replace("LANZAROTE\n", f"CAN-{suffix + 3}\n")
    text = text.replace("La Palma\n", f"CAN-{suffix + 4}\n")
    text = text.replace("LA PALMA\n", f"CAN-{suffix + 4}\n")
    text = text.replace("PALMAS (LAS)\n", f"CAN-{suffix + 4}\n")
    text = text.replace("Tenerife\n", f"CAN-{suffix + 5}\n")
    text = text.replace("TENERIFE\n", f"CAN-{suffix + 5}\n")
    text = text.replace("El Hierro\n", f"CAN-{suffix + 6}\n")
    text = text.replace("EL HIERRO\n", f"CAN-{suffix + 6}\n")
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
    text = _canarias_province_fix(text)
    return text


_CANARIAS_2011_05_LAST_NUMBER = None


@register_fixer("canarias", 2011, 5)
def fix_canarias_2011_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "Doña Venancio Pérez Hernández", "Doña Venancia Pérez Hernández"
    )
    text = text.replace("Noela García Ramos", "Noelia García Ramos")
    text = text.replace("Siglas: Nca", "Siglas: NCa")
    text = text.replace(
        "6 Don \nFeliz Andrés \nGonzález \nLorenzo",
        "6 Don \nFélix Andrés \nGonzález \nLorenzo",
    )
    text = text.replace(
        "1 Doña\nRosa\nRivero\nAbreu",
        "1 Doña\nRosi\nRivero\nAbreu",
    )
    text = text.replace(
        "Arturo Mario\nMéndez\nLloret",
        "Arturo Mario\nMéndez\nLlorens",
    )
    text = text.replace("Iglesias\nSangil", "Iglesias\nSan Gil")
    text = text.replace(
        "Anotomía Mª\nVera\nPerera",
        "Antonia María\nVera\nPerera",
    )
    # Fix OCR
    text = text.replace(".Marcuño", "Marcuño")
    text = text.replace("G11l", "Gil")
    text = text.replace("Aracel1", "Araceli")
    text = text.replace("BlázquezVidal", "Blázquez Vidal")
    text = text.replace("CarmeloRamírezÁlvarez", "Carmelo Ramírez Álvarez")
    text = text.replace("SantanaGarcía", "Santana García")
    text = text.replace("Nleves", "Nieves")
    text = text.replace("lone", "Ione")
    text = text.replace("PinoGonzález", "Pino González")
    text = text.replace("Doña Patricia 1. García Reyes", "Doña Patricia I. García Reyes")
    text = fix_maria_ocr(text)
    text = text.replace("7\nCandidatura número:\n", "Candidatura número: 7\n")
    text = text.replace("Don David Peñas López\nCandidatura número:\nDenominación: LOS VERDES", "Don David Peñas López\nCandidatura número: 5\nDenominación: LOS VERDES")
    text = text.replace("ES\nCandidatura número:\nDenominación: LOS VERDES", "ES\nCandidatura número: 5\nDenominación: LOS VERDES")
    text = text.replace("ES\nCandidatura número:\nDenominación: NUEVA CANARIAS", "ES\nCandidatura número: 7\nDenominación: NUEVA CANARIAS")
    text = text.replace("Candidatura número:\nDenominación: LOS VERDES", "Candidatura número: 4\nDenominación: LOS VERDES")
    text = text.replace("Candidatura número:\nDenominación: PARTIDO POPULAR", "Candidatura número: 2\nDenominación: PARTIDO POPULAR")
    text = text.replace(
        "ASAMBLEAS MUNICIPALES DE FUERTEVENTURA-NUEVA FUERTEVENTURA\n",
        "ASAMBLEAS MUNICIPALES DE FUERTEVENTURA-NUEVA FUERTEVENTURA ",
    )
    text = _canarias_province_fix(text)
    text = fix_multiline_candidacy_naming(text)
    global _CANARIAS_2011_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        LOWER_DON_CANDIDATE_NAME_REGEX,
        last_number=_CANARIAS_2011_05_LAST_NUMBER,
    )
    _CANARIAS_2011_05_LAST_NUMBER = last_number
    return text


_CANARIAS_2015_05_LAST_NUMBER = None


@register_fixer("canarias", 2015, 5)
def fix_canarias_2015_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "FRANCISCO GUZMAN RODRIGUEZ",
        "FRANCISCO GUZMAN RODRIGUEZ REYES",
    )
    text = text.replace(
        "NATALIA CURBELO CABRERO",
        "NATALIA CURBELO CABRERA",
    )
    # Other fixes to facilitate parsing
    text = fix_maria_ocr(text, upper=True)
    text = text.replace("PABLO l. GARCÍA HERNÁNDEZ", "PABLO I. GARCÍA HERNÁNDEZ")
    text = text.replace(
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-\n",
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-",
    )
    text = text.replace(
        "INICIATIVA POR EL HIERRO-IZQUIERDA UNIDA CANARIA-\n",
        "INICIATIVA POR EL HIERRO-IZQUIERDA UNIDA CANARIA-",
    )
    text = text.replace(
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-UNIDAD DEL\n",
        "CANARIAS DECIDE: IZQUIERDA UNIDA CANARIA-LOS VERDES-UNIDAD DEL ",
    )
    text = _canarias_province_fix(text)
    global _CANARIAS_2015_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        UPPER_CANDIDATE_REGEX,
        last_number=_CANARIAS_2015_05_LAST_NUMBER,
    )
    _CANARIAS_2015_05_LAST_NUMBER = last_number
    return text


_CANARIAS_2019_05_LAST_NUMBER = None


@register_fixer("canarias", 2019, 5)
def fix_canarias_2019_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA (CCa)",
        "CANDIDATURA NÚM.: 5. COALICIÓN CANARIA-PARTIDO NACIONALISTA CANARIO (CCa-PNC)",
    )
    # Facilitate parsing
    text = text.replace(
        "Circunscripción electoral: Autonómica", "Circunscripción electoral: Canarias"
    )
    text = text.replace(
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA (ANC) Y UNIDAD\n",
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA (ANC) Y UNIDAD ",
    )
    text = text.replace(
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA ANC y UNIDAD\n",
        "AHORA CANARIAS: ALTERNATIVA NACIONALISTA CANARIA ANC y UNIDAD ",
    )
    text = text.replace("5. JUNTA ELECTORAL", "JUNTA ELECTORAL")
    text = text.replace("MARÍA INMACULADA Pl MULET", "MARÍA INMACULADA PI MULET")
    text = text.replace("(PODEMOS\n", "(PODEMOS)\n")
    text = fix_maria_ocr(text, upper=True)
    # Fix missing numbers
    global _CANARIAS_2019_05_LAST_NUMBER
    text, last_number = number_candidates(
        text,
        UPPER_CANDIDATE_REGEX,
        last_number=_CANARIAS_2019_05_LAST_NUMBER,
    )
    _CANARIAS_2019_05_LAST_NUMBER = last_number
    text = _canarias_province_fix(text)
    return text


_CANARIAS_2023_05_LAST_NUMBER = None


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
        UPPER_CANDIDATE_REGEX,
        last_number=_CANARIAS_2023_05_LAST_NUMBER,
    )
    _CANARIAS_2023_05_LAST_NUMBER = last_number

    return text
