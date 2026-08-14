"""
Mapping file extracted from to the "infoelectoral" project by Jaime Gómez-Obregón (AGPL-3.0 license).

@copyright     Copyright (c) Jaime Gómez-Obregón
@link          https://github.com/JaimeObregon/infoelectoral
@license       https://www.gnu.org/licenses/agpl-3.0.en.html
"""

from common.models import ElectionType

PROVINCES = {
    "01": "Álava",
    "02": "Albacete",
    "03": "Alicante",
    "04": "Almería",
    "05": "Ávila",
    "06": "Badajoz",
    "07": "Baleares",
    "08": "Barcelona",
    "09": "Burgos",
    "10": "Cáceres",
    "11": "Cádiz",
    "12": "Castellón",
    "13": "Ciudad Real",
    "14": "Córdoba",
    "15": "A Coruña",
    "16": "Cuenca",
    "17": "Girona",
    "18": "Granada",
    "19": "Guadalajara",
    "20": "Guipúzcoa",
    "21": "Huelva",
    "22": "Huesca",
    "23": "Jaén",
    "24": "León",
    "25": "Lleida",
    "26": "La Rioja",
    "27": "Lugo",
    "28": "Madrid",
    "29": "Málaga",
    "30": "Murcia",
    "31": "Navarra",
    "32": "Ourense",
    "33": "Asturias",
    "34": "Palencia",
    "35": "Las Palmas",
    "36": "Pontevedra",
    "37": "Salamanca",
    "38": "Santa Cruz de Tenerife",
    "39": "Cantabria",
    "40": "Segovia",
    "41": "Sevilla",
    "42": "Soria",
    "43": "Tarragona",
    "44": "Teruel",
    "45": "Toledo",
    "46": "Valencia",
    "47": "Valladolid",
    "48": "Vizcaya",
    "49": "Zamora",
    "50": "Zaragoza",
    "51": "Ceuta",
    "52": "Melilla",
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
