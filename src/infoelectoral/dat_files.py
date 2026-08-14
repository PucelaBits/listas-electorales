"""Parses .DAT files from the Spanish Ministry of the Interior's electoral data."""

import os
import re
from collections.abc import Iterable
from dataclasses import dataclass

from common.models import ElectionType

from .code_mappings.mappings import ELECTION_TYPES


@dataclass(frozen=True)
class DATCandidacy:
    """Represents a candidacy extracted from a .DAT file."""

    code: str
    acronym: str
    name: str
    year: int
    month: int
    election_type: ElectionType


@dataclass(frozen=True)
class DATCandidate:
    """Represents a candidate extracted from a .DAT file."""

    candidacy_code: str
    repetition: int
    order: int
    substitute: bool
    name: str
    first_surname: str | None
    second_surname: str | None
    sex: str | None
    municipality_code: str
    province_code: str | None
    elected: bool


class DATParser:
    """Handles the parsing of fixed-width .DAT files."""

    def __init__(self, filepath: str):
        self.filepath = filepath
        filename = os.path.basename(filepath)
        match = re.search(r"(\d{2})(\d{2})(\d{2})(\d{2})\.DAT", filename, re.IGNORECASE)
        if not match:
            raise ValueError(f"Invalid filename format: {filename}")
        self.code = match.group(1)


class CandidacyDATParser(DATParser):
    """Handles the parsing of candidacy .DAT files."""

    def __init__(self, filepath: str):
        super().__init__(filepath)
        if self.code != "03":
            raise ValueError(f"Expected a candidacy file (03), but got {self.code}.")

    def parse(self) -> Iterable[DATCandidacy]:
        with open(self.filepath, "r", encoding="iso-8859-1") as f:
            for line in f:
                yield self.__parse_line(line)

    def __parse_line(self, line: str) -> DATCandidacy:
        """Parses a line from a Candidatures (03) file."""
        return DATCandidacy(
            code=line[8:14],
            acronym=line[14:64].strip(),
            name=line[64:214].strip(),
            year=int(line[2:6]),
            month=int(line[6:8]),
            election_type=ELECTION_TYPES.get(line[0:2]),
        )


class CandidateDATParser(DATParser):
    """Handles the parsing of candidate .DAT files."""

    def __init__(self, filepath: str):
        super().__init__(filepath)
        if self.code != "04":
            raise ValueError(f"Expected a candidate file (04), but got {self.code}.")

    def parse(self) -> Iterable[DATCandidate]:
        with open(self.filepath, "r", encoding="iso-8859-1") as f:
            for line in f:
                yield self.__parse_line(line)

    def __parse_line(self, line: str) -> DATCandidate:
        """Parses a line from a Candidates (04) file."""
        # Fix for corrupted records
        if line.startswith("042015051439153090873009TLinda"):
            line = line.replace("7000000001", "F00000000 ")

        return DATCandidate(
            candidacy_code=line[15:21],
            repetition=int(line[8:9]),
            order=int(line[21:24]),
            substitute=line[24:25] != "T",
            name=line[25:50].strip(),
            first_surname=line[50:75].strip() or None,
            second_surname=line[75:100].strip() or None,
            sex={"M": "M", "F": "F"}.get(line[100:101], None),
            province_code=None if line[9:11] == "99" else line[9:11],
            municipality_code=line[12:15],
            elected=line[119:120] == "S",
        )
