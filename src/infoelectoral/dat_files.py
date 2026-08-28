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


@dataclass(frozen=True)
class DATCandidate:
    """Represents a candidate extracted from a .DAT file."""

    year: int
    month: int
    election_type: ElectionType
    candidacy_code: str
    order: int
    substitute: bool
    full_name: str | None  # None for "derecho al olvido" cases
    sex: str | None
    municipality_code: str | None
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
            code=line[8:14], acronym=line[14:64].strip(), name=line[64:214].strip()
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
        """Parses a line from a Candidates (04) file.


        Adapted from "infoelectoral" project by Jaime Gómez-Obregón (AGPL-3.0 license).

        @copyright     Copyright (c) Jaime Gómez-Obregón
        @link          https://github.com/JaimeObregon/infoelectoral
        @license       https://www.gnu.org/licenses/agpl-3.0.en.html
        """
        # Fix for corrupted records
        if line.startswith("042015051439153090873009TLinda"):
            line = line.replace("7000000001", "F00000000 ")

        election_type = ELECTION_TYPES.get(line[0:2])
        year = int(line[2:6])
        month = int(line[6:8])

        # The name fields are split into 3 chunks of 25 characters starting at index 25
        name = line[25:50].rstrip()
        first_surname = line[50:75].rstrip()
        second_surname = line[75:100].rstrip()

        # Check if the record follows the modern format
        is_modern_format = (
            election_type != ElectionType.MUNICIPALES and year >= 2003
        ) or (year >= 2011)

        if is_modern_format:
            # Modern format: Join available parts with a single space
            parts = [p for p in (name, first_surname, second_surname) if p]
            full_name = " ".join(parts)
        else:
            # Old format: Check for overflowed chunks. If a chunk is exactly 25 chars,
            # the next chunk is a direct continuation (no space).
            full_name = name
            if first_surname:
                separator = "" if len(name) == 25 else " "
                full_name += separator + first_surname

                if second_surname:
                    separator = "" if len(first_surname) == 25 else " "
                    full_name += separator + second_surname

            full_name = full_name.strip()

        return DATCandidate(
            year=year,
            month=month,
            election_type=election_type,
            candidacy_code=line[15:21],
            order=int(line[21:24]),
            substitute=line[24:25] != "T",
            full_name=full_name
            if full_name
            else None,  # None for "derecho al olvido" cases
            sex={"M": "M", "F": "F"}.get(line[100:101], None),
            province_code=None if line[9:11] == "99" else line[9:11],
            municipality_code=None if line[12:15] == "999" else line[12:15],
            elected=line[119:120] == "S",
        )
