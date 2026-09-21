import re

from ._common import (
    LOWER_DON_CANDIDATE_NAME_REGEX,
    fix_missing_substitutes,
    register_fixer,
)


@register_fixer("galicia", 1997, 10)
def fix_galicia_1997_10(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace("Mª Luz Prieto Fernández", "María Luz Prieto Fernández")
    text = text.replace(
        "3.– María José Costas Fernández", "3.– Mª José Costas Fernández"
    )
    text = text.replace("20.– María José Segade Andrade", "20.– Mª José Segade Andrade")
    text = text.replace(
        "9.– Mª de las Mercedes Fortes Costas",
        "9.– María de las Mercedes Fortes Costas",
    )
    text = text.replace(
        "2.– Mª Antonia Pachón Moreno", "2.– María Antonia Pachón Moreno"
    )
    text = text.replace("1.– Mª Jesusa Escudero Lago", "1.– María Jesusa Escudero Lago")
    text = text.replace(
        "OFENSIVA NACIONAL SINDICALISTA (FGJONS)",
        "OFENSIVA NACIONAL SINDICALISTA (F.G. DE LAS JONS)",
    )
    text = text.replace("10.– Juan Alfonso Oubina", "10.– Juan Alfonso Oubiña")
    text = text.replace(
        "11.– María del Carmen Soliño Castro", "11.– Mª del Carmen Soliño Castro"
    )
    text = text.replace("2.– Cándido González Herrero", "2.– Cándido Gonzálvez Herrero")
    return text


_GALICIA_2009_03_CANDIDACY_REGEX = re.compile(r"^\*\s*(\d+)[\.|\s]?", re.MULTILINE)


@register_fixer("galicia", 2009, 3)
def fix_galicia_2009_03(text: str) -> str:
    text = text.replace("circunscrip-\n", "circunscrip")
    text = text.replace("circuns-\n", "circuns")
    # Errata (err.pdf)
    text = text.replace("15 Don Juan Francisco Ferreira González", "")
    text = text.replace("16 Dona Marta Mascato García", "15 Dona Marta Mascato García")
    text = text.replace("17 Don Antonio Goce Castro", "16 Don Antonio Goce Castro")
    text = text.replace("18 Dona Carmen Ansedes López", "17 Dona Carmen Ansedes López")
    text = text.replace(
        "19 Don Rafael Blanco Guerreiro", "18 Don Rafael Blanco Guerreiro"
    )
    text = text.replace(
        "20 Dona Begoña Domínguez Táboas", "19 Dona Begoña Domínguez Táboas"
    )
    text = text.replace(
        "21 Dona María Ángeles Conde Salgado", "20 Dona María Ángeles Conde Salgado"
    )
    text = text.replace(
        "22 Don José María Tobío Barreira", "21 Don José María Tobío Barreira"
    )
    text = text.replace(
        "-Suplentes:\n1 Don Luciano Eusebio Santiago Esperón\n2 Dona Alexandra Vidal Salgueiro\n3 Dona Irene Gurrea Conde\n4 Dona María Pilar Vidal González\n5 Don Manuel Barros Puente",
        "22 Don Luciano Eusebio Santiago Esperón\n-Suplentes:\n1 Dona Alexandra Vidal Salgueiro\n2 Dona Irene Gurrea Conde\n3 Dona María Pilar Vidal González\n4 Don Manuel Barros Puente",
    )
    # Facilitate parsing
    text = _GALICIA_2009_03_CANDIDACY_REGEX.sub(r"Candidatura núm. \1.", text)
    return text


@register_fixer("galicia", 2012, 10)
def fix_galicia_2012_10(text: str) -> str:
    # Facilitate parsing
    text = text.replace(
        "I. Relación de candidaturas proclamadas en la circunscripción electoral\n",
        "I. Relación de candidaturas proclamadas en la circunscripción electoral ",
    )
    text = fix_missing_substitutes(text, LOWER_DON_CANDIDATE_NAME_REGEX)
    return text
