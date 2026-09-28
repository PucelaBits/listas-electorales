import re

from common import NAME_WHITELIST_CHARS_LOWER, NAME_WHITELIST_CHARS_UPPER

from ._common import (
    fix_missing_substitute_numbers,
    fix_multiline_candidacy_naming,
    register_fixer,
)


@register_fixer("cataluna", 1999, 10)
def fix_cataluna_1999_10(text: str) -> str:
    # Errata (err.pdf)
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
    # Facilitate parsing
    text = text.replace("Formación política: ", "")
    text = text.replace("—4 Partido", "Candidatura núm. 4. Partido")
    # Add missing candidacy
    text = text.replace(
        "Candidatura núm. 7\nPartit dels Socialistes",
        "Candidatura núm. 6. RELLENO\nNO PROCLAMADA\nCandidatura núm. 7\nPartit dels Socialistes",
    )
    text = text.replace("—7 L luita Internacionalista: L I (L IT-CI)", "Candidatura núm. 6. RELLENO\nNO PROCLAMADA\n—7 Lluita Internacionalista: LI (LIT-CI)")
    return text


@register_fixer("cataluna", 2003, 11)
def fix_cataluna_2003_11(text: str) -> str:
    # Remove preamble
    if "principal e intereses ordinarios y moratorios" in text:
        text = text.split("blica la lista de candidaturas proclamadas para")[-1]
    # Errata (err.pdf)
    text = text.replace(
        "Candidatura núm. 3\nFormación política: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi (PSC-CpC)",
        "Candidatura núm. 3\nFormación política: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi (PSC (PSC-PSOE) - CpC)",
    )
    text = text.replace(
        "Candidatura núm. 2\nFormación política: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi (PSC-CpC)",
        "Candidatura núm. 2\nFormación política: Partit dels Socialistes de\nCatalunya - Ciutadans pel Canvi (PSC (PSC-PSOE)-CpC)",
    )
    text = text.replace(
        "Candidatura núm. 18\nFormación política: Estat Català\n1\nJordi Miro i Riba",
        "Candidatura núm. 18\nFormación política: Estat Català (EC)\n1\nJordi Miro i Riba",
    )
    text = text.replace(
        "16\nMaría Teresa Vinuesa López (Estat Català)",
        "Suplente:\n1\nMaría Teresa Vinuesa López (Estat Català)",
    )
    # Facilitate parsing
    text = text.replace("Gi-\n", "Gi")
    # Fix substitute declaration
    text = text.replace(
        "16 María Teresa Vinuesa López (Estat Català)",
        "SUPLENTES\n1. María Teresa Vinuesa López (Estat Català)",
    )
    return text


@register_fixer("cataluna", 2006, 11)
def fix_cataluna_2006_11(text: str) -> str:
    # Remove preamble
    if "CAREDA i dirigida pel lletrat JOSEP" in text:
        text = text.split("por el que se hacen públicas las candidaturas")[-1]
    # Errata (err.pdf)
    text = text.replace(
        "13. Josep Maria Freixenet i Mayans", "13. Josep Maria Freixanet i Mayans"
    )
    text = text.replace(
        "44. Antònia Serra i Baucells", "44. Antònia Serra i Baucells (Independent)"
    )
    text = text.replace(
        "44. Antònia Serra i Baucells (Independent) (Independent)",
        "44. Antònia Serra i Baucells (Independent)",
    )
    text = text.replace(
        "3. Xavier Vinyals i Capdepon", "3. Xavier Vinyals i Capdepon (Independent)"
    )
    text = text.replace(
        "3. Xavier Vinyals i Capdepon (Independent) (Independent)",
        "3. Xavier Vinyals i Capdepon (Independent)",
    )
    text = text.replace(
        "35. José Antonio García Balllester (Ind)",
        "35. José Antonio García Ballester (Ind)",
    )
    text = text.replace("6. Abert Camarasa Escubedo", "6. Albert Camarasa Escubedo")
    text = text.replace(
        "70. Monserrat Cervera Casanueva", "70. Montserrat Cervera Casanueva"
    )
    text = text.replace(
        "38. Maria de la torre i Prieto", "38. Maria de la Torre i Prieto"
    )
    old_block = (
        "1. Francesc Corbella Valea\n"
        "2. Maria Dolors Ivorra Cano\n"
        "3. Rafael Lopez Urgel\n"
        "4. Eva Maria Álvarez Moya\n"
        "5. Víctor Abella Salido\n"
        "6. Alexandra Fernandez Ruiz\n"
        "7. Graciela Medina Esquivel\n"
        "8. Damaris Moran Perez\n"
        "9. Pedro Garrote Vilchez\n"
        "10. Maria Cinta Escriche Matheu\n"
        "11. Gerard Font Izquierdo\n"
        "12. Ana Artazcoz Sastre\n"
        "13. Xavier Frias Roman\n"
        "14. Yasmina Andujar Vazquez\n"
        "15. José Manuel Gomez Arribas\n"
        "16. Maria Lucia Jurado Pouso\n"
        "17. Francisca Jimenez Cozar"
    )
    new_block = (
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
    )
    text = text.replace(old_block, new_block)
    # Facilitate parsing
    text = text.replace("Provincial\n", "Provincial ")
    text = text.replace("CANDIDATURA REGISTRADA AMB EL NÚMERO", "CANDIDATURA NÚM.")
    # Add missing candidacy number
    text = text.replace(
        "CANDIDATURA NÚM. 16\nPARTIT REPUBLICÀ CATALÀ",
        "CANDIDATURA NÚM. 15. RELLENO\nNO PROCLAMADA\nCANDIDATURA NÚM. 16. PARTIT REPUBLICÀ CATALÀ",
    )
    text = text.replace(
        "CANDIDATURA NÚM. 18\nMOVIMIENTO SOCIAL REPUBLICANO",
        "CANDIDATURA NÚM. 17. RELLENO\nNO PROCLAMADA\nCANDIDATURA NÚM. 18. MOVIMIENTO SOCIAL REPUBLICANO",
    )
    return text


@register_fixer("cataluna", 2010, 11)
def fix_cataluna_2010_11(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("Sra. Soledat Guasch Duran", "Sra. Soledat Gasch Duran")
    text = text.replace("Sra. Soledat guasch Duran", "Sra. Soledat Gasch Duran")
    return text


_CATALUNA_2015_09_CANDIDATE_RE = re.compile(
    rf"(?:[{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER}]+ )+[{NAME_WHITELIST_CHARS_UPPER}][{NAME_WHITELIST_CHARS_LOWER}]+$"
)

_CATALUNA_2015_09_LLEIDA_CANDIDACY_RE = re.compile(
    rf"^(?:[{NAME_WHITELIST_CHARS_UPPER}]+[ ,]+)+.+[\r?\n]TITULARES", re.MULTILINE
)

_CATALUNA_2015_09_LLEIDA_CANDIDACY_INDEX = 0


@register_fixer("cataluna", 2015, 9)
def fix_cataluna_2015_09(text: str) -> str:
    text = fix_missing_substitute_numbers(text, _CATALUNA_2015_09_CANDIDATE_RE)
    text = fix_multiline_candidacy_naming(text)
    text = text.replace(
        "NÚM. DE ORDEN\n9\nFORMACIÓN POLÍTICA:\nCATALUNYA SÍ QUE ES POT",
        "Candidatura número: 9. FORMACIÓN POLÍTICA:\nCATALUNYA SÍ QUE ES POT (CatSíqueesPot)",
    )
    global _CATALUNA_2015_09_LLEIDA_CANDIDACY_INDEX
    for match in _CATALUNA_2015_09_LLEIDA_CANDIDACY_RE.finditer(text):
        _CATALUNA_2015_09_LLEIDA_CANDIDACY_INDEX += 1
        text = text.replace(
            match.group(0),
            f"Candidatura número: {_CATALUNA_2015_09_LLEIDA_CANDIDACY_INDEX}. {match.group(0)}",
        )
    return text


@register_fixer("cataluna", 2017, 12)
def fix_cataluna_2017_12(text: str) -> str:
    text = fix_multiline_candidacy_naming(text)
    return text


@register_fixer("cataluna", 2021, 2)
def fix_cataluna_2021_02(text: str) -> str:
    # Remove preamble
    text = text.replace(
        "PER UN MÓN MÉS JUST\nSIGLAS:", "PER UN MÓN MÉS JUST\nSIGLAS:\nPUM+J"
    )
    text = fix_multiline_candidacy_naming(text)
    # Remove duplicate in Catalan
    for page in range(15, 29):
        if f"{page}/28" in text:
            return ""
    # Fix missing candidacy
    text = text.replace(
        "6.- JUNTS PER CATALUNYA (JxCat)",
        "Candidatura número: 5. RELLENO\nNO PROCLAMADA\n6.- JUNTS PER CATALUNYA (JxCat)",
    )
    # Fix ambiguous candidacy
    text = text.replace(
        "11.- VOX (VOX)",
        "Candidatura número: 10. RELLENO\nNO PROCLAMADA\nCandidatura número: 11. VOX (VOX)",
    )
    # Fix missing candidacy
    text = text.replace(
        "14.- IZQUIERDA EN POSITIVO (IZQP)",
        "Candidatura número: 13. RELLENO\nNO PROCLAMADA\n14.- IZQUIERDA EN POSITIVO (IZQP)",
    )
    text = text.replace(
        "18.- MOVIMENT PRIMÀRIES PER LA INDEPENDÈNCIA DE CATALUNYA (MPIC)",
        "Candidatura número: 15. RELLENO\nNO PROCLAMADA\nCandidatura número: 16. RELLENO\nNO PROCLAMADA\nCandidatura número: 17. RELLENO\nNO PROCLAMADA\n18.- MOVIMENT PRIMÀRIES PER LA INDEPENDÈNCIA DE CATALUNYA (MPIC)",
    )
    text = text.replace(
        "22. RECORTES CERO-GRUP VERD-MUNICIPALISTES (RECORTES CERO-GV-M)",
        "Candidatura número: 21. RELLENO\nNO PROCLAMADA\n22. RECORTES CERO-GRUP VERD-MUNICIPALISTES (RECORTES CERO-GV-M)",
    )
    return text


@register_fixer("cataluna", 2024, 5)
def fix_cataluna_2024_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "ESQUERRA REPUBLICANA DE CATALUNYA (ERC / ESQUERRA)",
        "ESQUERRA REPUBLICANA DE CATALUNYA (ERC)",
    )
    return text
