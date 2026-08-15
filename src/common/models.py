from dataclasses import dataclass
from enum import Enum
from typing import Literal


@dataclass(frozen=True)
class Candidacy:
    """Represents information about a candidacy (i.e. political party)."""

    acronym: str
    name: str


@dataclass(frozen=True)
class Candidate:
    """Represents information about a candidate."""

    candidacy: Candidacy
    order: int
    full_name: str
    sex: Literal["M", "F", "O"] | None
    elected: bool
    substitute: bool
    province: str | None
    municipality: str | None


class ElectionType(Enum):
    """Enumeration for different types of elections."""

    REFERENDUM = "referendum"
    CONGRESO = "congreso"
    SENADO = "senado"
    MUNICIPALES = "municipales"
    AUTONOMICAS = "autonomicas"
    CABILDOS = "cabildos"
    PARLAMENTO_EUROPEO = "parlamento_europeo"
    PARTIDOS_JUDICIALES_DIPUTACIONES = "partidos_judiciales_diputaciones"
    JUNTAS_GENERALES = "juntas_generales"


@dataclass(frozen=True)
class Election:
    """Represents a collection of candidates for a specific election."""

    year: int
    month: int
    repetition: int
    type: ElectionType
    candidates: tuple[Candidate]
