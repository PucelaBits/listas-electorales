"""
Mapping file extracted from to the "infoelectoral" project by Jaime Gómez-Obregón (AGPL-3.0 license).

@copyright     Copyright (c) Jaime Gómez-Obregón
@link          https://github.com/JaimeObregon/infoelectoral
@license       https://www.gnu.org/licenses/agpl-3.0.en.html
"""

from common import PROVINCES_LIST
from common.models import ElectionType

PROVINCES = {
    "01": PROVINCES_LIST[0],
    "02": PROVINCES_LIST[1],
    "03": PROVINCES_LIST[2],
    "04": PROVINCES_LIST[3],
    "05": PROVINCES_LIST[4],
    "06": PROVINCES_LIST[5],
    "07": PROVINCES_LIST[6],
    "08": PROVINCES_LIST[7],
    "09": PROVINCES_LIST[8],
    "10": PROVINCES_LIST[9],
    "11": PROVINCES_LIST[10],
    "12": PROVINCES_LIST[11],
    "13": PROVINCES_LIST[12],
    "14": PROVINCES_LIST[13],
    "15": PROVINCES_LIST[14],
    "16": PROVINCES_LIST[15],
    "17": PROVINCES_LIST[16],
    "18": PROVINCES_LIST[17],
    "19": PROVINCES_LIST[18],
    "20": PROVINCES_LIST[19],
    "21": PROVINCES_LIST[20],
    "22": PROVINCES_LIST[21],
    "23": PROVINCES_LIST[22],
    "24": PROVINCES_LIST[23],
    "25": PROVINCES_LIST[24],
    "26": PROVINCES_LIST[25],
    "27": PROVINCES_LIST[26],
    "28": PROVINCES_LIST[27],
    "29": PROVINCES_LIST[28],
    "30": PROVINCES_LIST[29],
    "31": PROVINCES_LIST[30],
    "32": PROVINCES_LIST[31],
    "33": PROVINCES_LIST[32],
    "34": PROVINCES_LIST[33],
    "35": PROVINCES_LIST[34],
    "36": PROVINCES_LIST[35],
    "37": PROVINCES_LIST[36],
    "38": PROVINCES_LIST[34],
    "39": PROVINCES_LIST[37],
    "40": PROVINCES_LIST[38],
    "41": PROVINCES_LIST[39],
    "42": PROVINCES_LIST[40],
    "43": PROVINCES_LIST[41],
    "44": PROVINCES_LIST[42],
    "45": PROVINCES_LIST[43],
    "46": PROVINCES_LIST[44],
    "47": PROVINCES_LIST[45],
    "48": PROVINCES_LIST[46],
    "49": PROVINCES_LIST[47],
    "50": PROVINCES_LIST[48],
    "51": PROVINCES_LIST[49],
    "52": PROVINCES_LIST[50],
}

ELECTION_TYPES = {
    "01": ElectionType.REFERENDUM,
    "02": ElectionType.CONGRESO,
    "03": ElectionType.SENADO,
    "04": ElectionType.MUNICIPALES,
    "05": ElectionType.AUTONOMICAS,
    "06": ElectionType.CABILDOS,
    "07": ElectionType.PARLAMENTO_EUROPEO,
    "10": ElectionType.PARTIDOS_JUDICIALES_DIPUTACIONES,
    "15": ElectionType.JUNTAS_GENERALES,
}
