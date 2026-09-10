import re
from dataclasses import replace

from common import logger
from common.models import Candidacy, Candidate
from common.names import prettify_name

from .pdf import PDFReader

_CANDIDATE_TRAILING_CHARS_RE = re.compile(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\-\(\)'\.]{1,2}\b$")
_CANDIDATE_BEGINNING_CHARS_RE = re.compile(r"^\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\-\(\)'\.]{1,2}\b")
_EXTRA_WHITESPACE_RE = re.compile(r"\s{2,}")
_CANDIDATE_WHITELIST_RE = re.compile(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ \-'\(\)\.]")
_DATE_RE = re.compile(
    r"(?i)\b(0?[1-9]|[12][0-9]|3[01])\s+?(?:de\s+)?(enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre)(?:\s+(?:de\s+)?\d{4})?\b\.?"
)
_DATE_NUMBER_RE = re.compile(r"\b(?:\d{4}[\-/]\d{2}[\-/]\d{2}|(?:\d{2}[\-/]\d{2}[\-/]\d{4}))\b")

# Extract candidacy name and acronym
_CANDIDACY_RE = re.compile(
    r"^(.*?)"
    r"[\s.,-]*"
    r"(?:"
    r"([A-ZÑ0-9]+\.[A-ZÑ0-9.\-]*\s*\([^()]+\))"
    r"|"
    r"\(([^()]+(?:\([^()]*\)[^()]*)*)\)"
    r")$"
)


def _extract_candidacy(content: str) -> tuple[str, str]:
    content = content.strip()
    match = _CANDIDACY_RE.search(content)
    # TODO: Improve this with examples
    # FALANGE ESPAÑOLA DE LAS J.O.N.S. (F.E. DE LAS J.O.N.S.)
    # PARTIDO COMUNISTA DE ESPAÑA (MARXISTA-LENINISTA) P.C. (M-L)
    # TODO: Handle dots like
    # PARTIDO SOCIALISTA.

    if match:
        # Strip string again to catch any edge-case punctuation at the boundaries
        party = match.group(1).strip(" .,-")

        # The acronym will be captured by either Branch A (group 2) or Branch B (group 3)
        acronym = match.group(2) or match.group(3)

        return party, acronym.strip()

    return content, ""


def _clean_candidate_name(name: str) -> str:
    # Keep just standard letters, Spanish accents, eñes, ü, spaces, hyphens, and apostrophes
    name = re.sub(_CANDIDATE_WHITELIST_RE, " ", name)
    # If the name starts with "D ", it is actually "D. "
    if name.startswith("D.a "):
        name = name[3:]
    elif name.startswith(("D ", "D.")):
        name = name[2:]
    # Remove any trailing random letters (< 3 characters) that are likely OCR artifacts
    name = re.sub(_CANDIDATE_TRAILING_CHARS_RE, "", name)
    # Remove any leading random letters (< 3 characters) that are likely OCR artifacts
    name = re.sub(_CANDIDATE_BEGINNING_CHARS_RE, "", name)
    # Remove any double spaces or extra whitespace
    name = re.sub(_EXTRA_WHITESPACE_RE, " ", name)
    # The split of the name into parts should be more than 3
    if len(name.split()) < 3:
        raise ValueError(f"Detected candidate '{name}' with too short name.")
    return name.strip()


def _has_trash_text(line: str) -> bool:
    line_lower = line.lower()
    return (
        "http" in line_lower
        or "página" in line_lower
        or "apellidos" in line_lower
        or "secretaría" in line_lower
        or "sucursal" in line_lower
        or "teléfono" in line_lower
        or "boletín oficial" in line_lower
        or _DATE_RE.search(line_lower) is not None
        or _DATE_NUMBER_RE.search(line_lower) is not None
    )


class TextElectionParser:
    PROVINCE_RE = re.compile(
        r"(?:JUNTA ELECTORAL\s+PROVINCIAL\s+DE\s+|CIRCUNSCRIPCI[ÓO]N\s+ELECTORAL:\s+|PROVINCIA\s+DE\s+)([A-ZÁÉÍÓÚÑ\s]+)",
        re.IGNORECASE,
    )

    NOT_PROCLAMATED_RE = re.compile(
        r"NO\s+PROCLAMADA",
        re.IGNORECASE,
    )

    # Extract explicit candidacy headers
    EXPLICIT_CANDIDACY_RE = re.compile(
        r"^Candidatura\s+n[úu]m(?:ero)?\.?:?\s*(\d+)[\s\.\-\–\—~]?\s+(.+)$",
        re.IGNORECASE,
    )

    # Numbered items
    NUMBERED_ITEM_RE = re.compile(
        r"^[\s\.\-\–\—~]?\s*(?:Nº\s*|No\s+|N\s+|N\.O?\s*|Núm[\.:]\s*|Num[\.:]\s*)?(\d+)\s?[\s\.\-\–\—~:]+\s*([a-zA-ZáéíóúÁÉÍÓÚñÑüÜ]+.+)$",
        re.IGNORECASE,
    )

    # Catch isolated numbers sitting on their own line
    ISOLATED_NUMBER_RE = re.compile(
        r"^(?:Candidatura\s+n[úu]m(?:ero)?\.?:?\s*)?(\d+)[ \.\-\–\—~]+$", re.IGNORECASE
    )

    # Catch lines that have multiple numbers and names separated by whitespace
    MULTI_LINE_SPLIT_RE = re.compile(r"\s+(?=\d+[ \.\-\–\—~:]+\s+)")

    SUPLENTE_RE = re.compile(r"^Suplentes?:?", re.IGNORECASE)

    def __init__(self, text_reader: PDFReader):
        self.text_reader = text_reader
        self.parsed_data = []
        self.current_province = ""
        self.current_candidacy = None
        self.candidacy_order = 0
        self.is_substitute = False
        self.candidate_order = 0
        # Temporarily store the order number if we encounter an isolated number on a line by itself
        self.pending_order = None
        self.line_completed = False

    def parse(self):
        prev_line = None
        for line in self.text_reader.parse():
            if prev_line is None:
                prev_line = line.strip()
                continue
            line = line.strip()
            self.__process_line(prev_line, line)
            prev_line = line
        # Process the last line
        self.__process_line(prev_line, "")
        if len(self.parsed_data) == 0:
            raise ValueError("No candidates found")

    def build(self) -> tuple[Candidate]:
        return tuple(self.parsed_data)

    def __process_line(self, line: str, next_line: str) -> None:
        """Evaluates a single line and routes it to the appropriate state handler."""
        print(f"Processing line: {line}")  # Debugging output
        if _has_trash_text(line):
            logger.debug(f"Discarding trash line: {line}")
            self.line_completed = True
            return

        # Province
        prov_match = self.PROVINCE_RE.search(line)
        if prov_match:
            self.current_province = prov_match.group(1).strip().title()
            logger.debug(f"Detected province: {self.current_province}")
            # Change of province indicates a new candidacy section, so reset candidacy and candidate order
            self.line_completed = True
            self.__mark_candidacy_as_finished()
            # Reset expected candidacy order for a new province
            self.candidacy_order = 0
            return

        # Explicit line candidacy headers (e.g., "Candidatura núm.: 1 Partido XYZ")
        candidacy_match = self.EXPLICIT_CANDIDACY_RE.match(line)
        if candidacy_match:
            order = int(candidacy_match.group(1))
            content = candidacy_match.group(2).strip()
            self.__set_candidacy(order, content)
            return

        if self.NOT_PROCLAMATED_RE.match(line):
            if self.current_candidacy is None:
                raise ValueError(
                    "Found 'NO PROCLAMADA' line while parsing, but no current candidacy is set."
                )
            # Make sure no candidates were parsed for the current candidacy before resetting
            if (
                len(self.parsed_data) > 0
                and self.parsed_data[-1].candidacy == self.current_candidacy
            ):
                raise ValueError(
                    f"Found 'NO PROCLAMADA' line while parsing candidates for {self.current_candidacy}, but candidates were already parsed."
                )
            # Reset the current candidacy
            self.__reset_candicacy()
            return

        # Substitutes
        if self.SUPLENTE_RE.match(line):
            if len(self.parsed_data) == 0:
                raise ValueError(
                    "Substitute section found before any candidates were parsed."
                )
            self.is_substitute = True
            self.pending_order = None
            self.line_completed = True
            if self.MULTI_LINE_SPLIT_RE.search(line):
                self.__process_multiple_lines(line, next_line)
            return

        # Numbered items (implicit candidate or candidacy if old format)
        item_match = self.NUMBERED_ITEM_RE.match(line)
        if item_match:
            # If the line contains multiple candidates or candidacies, split it and process each part
            if self.MULTI_LINE_SPLIT_RE.search(line):
                self.__process_multiple_lines(line, next_line)
                return
            order = int(item_match.group(1))
            content = item_match.group(2).strip()
            self.__handle_numbered_item(order, content, next_line)
            self.pending_order = None
            return

        # If we caught an isolated number on the previous line, this line is the name
        if self.pending_order is not None:
            logger.debug(
                f"Detected isolated number on previous line. Using pending order {self.pending_order} for current line: {line}"
            )
            self.__handle_numbered_item(self.pending_order, line, next_line)
            self.pending_order = None
            return

        # Numbered items (split-line format)
        isolated_match = self.ISOLATED_NUMBER_RE.match(line)
        if isolated_match:
            expected_order = int(isolated_match.group(1))
            if expected_order < 100:  # Arbitrary threshold to avoid false positives
                self.pending_order = expected_order
            return

        # Handle multi-line continuations and discard decorations
        if (
            not re.search(r"\d", line)
            and "núm." not in line.lower()
            and not self.line_completed
            and len(line) > 1
        ):
            self.__handle_unmatched_line(line)
            return
        # Mark the line as completed to avoid adding more stuff to the last candidate
        self.line_completed = True

    def __process_multiple_lines(self, line: str, next_line: str) -> None:
        sub_lines = self.MULTI_LINE_SPLIT_RE.split(line)
        prev_line = None
        for sub_line in sub_lines:
            if prev_line is None:
                prev_line = sub_line.strip()
                continue
            sub_line = sub_line.strip()
            self.__process_line(prev_line, sub_line)
            prev_line = sub_line
        # Process the last sub-line
        if prev_line is not None:
            self.__process_line(prev_line, next_line)

    def __handle_numbered_item(self, order: int, content: str, next_line: str) -> None:
        """Processes lines that start with a number (either a candidacy or a candidate)."""
        if "disposiciones generales" in content.lower():
            # Skip lines that are part of the general provisions section
            return
        if order > 100:  # Arbitrary threshold to avoid false positives
            return
        if (
            order == 1
            and self.candidate_order > 0
            and (
                not self.is_substitute
                or (
                    self.is_substitute
                    and len(self.parsed_data) > 0
                    and self.parsed_data[-1].substitute
                )
            )
        ):
            raise ValueError(
                "Unexpected new candidate with order 1 while already parsing candidates."
            )
        if order == 1 and self.current_candidacy is None:
            if self.candidacy_order != 0:
                raise ValueError(
                    f"Unexpected candidacy order {order} when actually expected {self.candidacy_order} in first candidacy."
                )
            # We are starting the first candidacy in the document
            self.__set_candidacy(order, content)
            return

        if order == self.candidate_order + 1 and order == self.candidacy_order + 1:
            logger.debug(
                f"Ambiguous order {order} found. This could be either a new candidacy or a candidate for the current candidacy. Next line: {next_line}"
            )
            # This is either a candidate or a new candidacy
            # Look at the start of the next line to determine if it's a candidate or a new candidacy
            # There could be still other stuff that messes with the parsing, so we manually fix those
            next_number_match = self.NUMBERED_ITEM_RE.match(next_line)
            next_isolated_match = self.ISOLATED_NUMBER_RE.match(next_line)
            if (
                (next_number_match and next_number_match.group(1) == "1")
                or (next_isolated_match and next_isolated_match.group(1) == "1")
                or re.match(self.NOT_PROCLAMATED_RE, next_line)
            ):
                # This is a new candidacy
                self.__set_candidacy(order, content)
            else:
                # This is a candidate for the current candidacy
                self.__add_candidate(content, order)
            return

        if order == self.candidate_order + 1:
            # We expect to be parsing candidates for the current candidacy
            self.__add_candidate(content, order)
            return
        # Check if we have switched to substitutes
        if (
            order == 1
            and self.is_substitute
            and len(self.parsed_data) > 0
            and not self.parsed_data[-1].substitute
        ):
            # We have switched to substitutes for the current candidacy
            self.__add_candidate(content, order)
            return

        if self.candidacy_order + 1 == order:
            # We have switched to a new candidacy
            self.__set_candidacy(order, content)
            return
        raise ValueError(
            f"Unexpected order {order} when actually expected candidacy ({self.candidacy_order + 1}) or candidate ({self.candidate_order + 1})."
        )

    def __set_candidacy(self, order: int, content: str) -> None:
        """Extracts and sets the current candidacy."""
        if len(self.parsed_data) == 0 and self.current_candidacy is not None:
            raise ValueError("Candidacy set before any candidates were parsed.")
        self.__mark_candidacy_as_finished()
        current_party, current_acronym = _extract_candidacy(content)
        self.current_candidacy = Candidacy(name=current_party, acronym=current_acronym)
        self.candidacy_order = order
        logger.debug(f"Set current candidacy: {self.current_candidacy}")
        self.line_completed = False  # Reset line completion for new candidacy
        # We have switched to a new candidacy, so reset order and substitute flags
        self.is_substitute = False
        self.candidate_order = 0
        self.pending_order = None

    def __add_candidate(self, content: str, order: int) -> None:
        """Cleans candidate data and appends it to the dataset."""
        if not self.current_candidacy:
            raise ValueError(
                "Unexpected candidate without a current candidacy context."
            )
        if not self.current_province:
            raise ValueError("Unexpected candidate without a current province context.")
        candidate = Candidate(
            full_name=prettify_name(_clean_candidate_name(content)),
            candidacy=self.current_candidacy,
            province=self.current_province,
            order=order,
            substitute=self.is_substitute,
            sex=None,
            elected=None,
            municipality=None,
        )
        logger.debug(
            f"Adding candidate: {candidate.full_name} from {candidate.province} for {candidate.candidacy.name} {'(substitute)' if candidate.substitute else ''}"
        )
        self.parsed_data.append(candidate)
        self.candidate_order = order
        self.line_completed = False  # Reset line completion for new candidate

    def __handle_unmatched_line(self, line: str) -> None:
        """Discards headers/footers or appends valid multi-line names."""
        # Append valid continuation to the last recorded candidate
        if len(self.parsed_data) > 0 and self.candidate_order > 0:
            if self.parsed_data[-1].full_name.endswith("-") and line[0].islower():
                # Handle hyphenated names that are split across lines
                new_name = _clean_candidate_name(
                    self.parsed_data[-1].full_name[:-1] + line
                )
            else:
                new_name = _clean_candidate_name(
                    self.parsed_data[-1].full_name + " " + line
                )
            self.parsed_data[-1] = replace(
                self.parsed_data[-1],
                full_name=prettify_name(new_name),
            )
        elif self.current_candidacy and self.candidate_order == 0:
            # If we are not currently parsing candidates, this line is a continuation of the candidacy name
            # TODO: This might join names with "-" incorrectly
            if self.current_candidacy.name.endswith("-"):
                full_content = self.current_candidacy.name[:-1] + line
            else:
                full_content = self.current_candidacy.name + " " + line
            new_name, new_acronym = _extract_candidacy(full_content)
            self.current_candidacy = replace(
                self.current_candidacy, name=new_name, acronym=new_acronym
            )

    def __validate_candidates_count(self) -> None:
        """Validates that the number of candidates matches the expected count for the previous candidacy."""
        expected_candidates = 0
        previous_candidacy = None
        for c in self.parsed_data[::-1]:
            if c.substitute:
                continue  # Skip substitutes when counting candidates
            if c.candidacy == self.current_candidacy:
                expected_candidates += 1
            else:
                break
        if expected_candidates == 0:
            raise ValueError(
                f"No candidates found for {self.current_candidacy.name} in {self.current_province}"
            )
        # Search for the previous candidacy in the parsed data
        start_index = expected_candidates
        for c in self.parsed_data[-expected_candidates - 1 :: -1]:
            if c.candidacy != self.current_candidacy:
                previous_candidacy = c.candidacy
                previous_province = c.province
                break
            start_index += 1
        # Calculate the candidates of the previous candidacy to compare with the current one
        if previous_candidacy is None:
            return  # No previous candidacy to compare with
        if previous_province != self.current_province:
            return  # Different province, no need to compare
        previous_candidates = 0
        for c in self.parsed_data[-start_index - 1 :: -1]:
            if c.substitute:
                continue  # Skip substitutes when counting candidates
            if c.candidacy == previous_candidacy:
                previous_candidates += 1
            else:
                break
        if previous_candidates == 0:
            raise ValueError(
                f"Unexpected 0 candidates found for previous candidacy {previous_candidacy.name} in {self.current_province}"
            )
        if previous_candidates != expected_candidates:
            raise ValueError(
                f"Mismatch in number of candidates between {previous_candidacy.name} "
                f"({previous_candidates}) and {self.current_candidacy.name} "
                f"({expected_candidates}) in {self.current_province}"
            )

    def __mark_candidacy_as_finished(self) -> None:
        """Marks the current candidacy as finished and resets relevant state."""
        if self.current_candidacy is None:
            return
        self.__validate_candidates_count()
        # If we were parsing substitutes, ensure at least one substitute was found for the current candidacy
        if self.is_substitute and (
            self.parsed_data is None or not self.parsed_data[-1].substitute
        ):
            raise ValueError(
                f"No substitutes found for {self.current_candidacy.name} in {self.current_province}"
            )
        self.__reset_candicacy()

    def __reset_candicacy(self) -> None:
        """Resets the current candidacy and related state."""
        self.current_candidacy = None
        self.candidate_order = 0
        self.pending_order = None
        self.is_substitute = False
