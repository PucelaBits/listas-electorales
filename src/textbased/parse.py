import re
from dataclasses import replace

from common import logger
from common.models import Candidacy, Candidate
from common.names import prettify_name

from .pdf import PDFReader

_CANDIDATE_TRAILING_CHARS_RE = re.compile(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\-\(\)']{1,2}\b$")
_CANDIDATE_WHITELIST_RE = re.compile(r"[^a-zA-ZáéíóúÁÉÍÓÚñÑüÜ \-'\(\)]")

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

    if match:
        # Strip string again to catch any edge-case punctuation at the boundaries
        party = match.group(1).strip(" .,-")

        # The acronym will be captured by either Branch A (group 2) or Branch B (group 3)
        acronym = match.group(2) or match.group(3)

        return party, acronym.strip()

    return content, ""


def _clean_candidate_name(name: str) -> str:
    # Keep just standard letters, Spanish accents, eñes, ü, spaces, hyphens, and apostrophes
    name = re.sub(_CANDIDATE_WHITELIST_RE, "", name)
    # Remove any trailing random letters (< 3 characters) that are likely OCR artifacts
    name = re.sub(_CANDIDATE_TRAILING_CHARS_RE, "", name)
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
        or " enero" in line_lower
        or "febrero" in line_lower
        or "marzo" in line_lower
        or "junio" in line_lower
        or "agosto" in line_lower
        or "septiembre" in line_lower
        or "noviembre" in line_lower
        or "diciembre" in line_lower
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
        r"^Candidatura\s+n[úu]m\.?:\s*\d+[ \.\-\–]+\s+(.+)$", re.IGNORECASE
    )

    # Numbered items
    NUMBERED_ITEM_RE = re.compile(r"^(\d+)[ \.\-\–]+\s+(.+)$", re.IGNORECASE)

    # Catch isolated numbers sitting on their own line
    ISOLATED_NUMBER_RE = re.compile(r"^(\d+)[ \.\-\–]+$")

    # Catch lines that have multiple numbers and names separated by whitespace
    MULTI_LINE_SPLIT_RE = re.compile(r"\s+(?=\d+[ \.\-\–]+\s+)")

    SUPLENTE_RE = re.compile(r"^Suplentes?:?", re.IGNORECASE)

    def __init__(self, text_reader: PDFReader):
        self.text_reader = text_reader
        self.parsed_data = []
        self.current_province = ""
        self.current_candidacy = None
        self.is_substitute = False
        self.candidate_order = 0
        # Temporarily store the order number if we encounter an isolated number on a line by itself
        self.pending_order = None
        self.line_completed = False
        self.expected_substitutes = None
        self.__reset_state()

    def __reset_state(self) -> None:
        """Resets the parser's state for a new PDF file."""
        self.current_province = ""
        self.current_candidacy = None
        self.is_substitute = False
        self.candidate_order = 0
        self.pending_order = None
        self.line_completed = False
        self.expected_substitutes = None

    def parse(self):
        for line in self.text_reader.parse():
            self.__process_line(line.strip())
        if len(self.parsed_data) == 0:
            raise ValueError("No candidates found")

    def build(self) -> tuple[Candidate]:
        # TODO: Perform a cleanup of the parsed data to remove any duplicates candidates
        return tuple(self.parsed_data)

    def __process_line(self, line: str) -> None:
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
            return

        # Explicit line candidacy headers (e.g., "Candidatura núm.: 1 Partido XYZ")
        candidacy_match = self.EXPLICIT_CANDIDACY_RE.match(line)
        if candidacy_match:
            content = candidacy_match.group(1).strip()
            self.__set_candidacy(content)
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
            # Remove the current candidacy
            self.__mark_candidacy_as_finished()
            return

        # If the line contains multiple candidates or candidacies, split it and process each part
        if self.MULTI_LINE_SPLIT_RE.search(line):
            sub_lines = self.MULTI_LINE_SPLIT_RE.split(line)
            for sub_line in sub_lines:
                if sub_line.strip():
                    self.__process_line(sub_line.strip())
            return

        # If we caught an isolated number on the previous line, this line is the name
        if self.pending_order is not None:
            self.__handle_numbered_item(self.pending_order, line)
            self.pending_order = None
            return

        # Numbered items (implicit candidate or candidacy if old format)
        item_match = self.NUMBERED_ITEM_RE.match(line)
        if item_match:
            order = int(item_match.group(1))
            content = item_match.group(2).strip()
            self.__handle_numbered_item(order, content)
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

    def __handle_numbered_item(self, order: int, content: str) -> None:
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
            # We are starting the first candidacy in the document
            self.__set_candidacy(content)
            return

        if order == self.candidate_order + 1:
            if (
                self.is_substitute
                and self.expected_substitutes is not None
                and order == self.expected_substitutes + 1
            ):
                # In some PDFs, the candidacies are not separated by the a different title,
                # so it can be mistaken as a new candidate. We are actually starting a new candidacy
                logger.debug(
                    f"Automatically detected new candidacy after {self.expected_substitutes} substitutes for {self.current_candidacy.name}. Setting new candidacy: {content}"
                )
                self.__set_candidacy(content)
                return
            # We expect to be parsing candidates for the current candidacy
            self.__add_candidate(content, order)
            self.candidate_order = order
        else:
            # Check if we have switched to substitutes or a new candidacy
            if (
                self.is_substitute
                and len(self.parsed_data) > 0
                and not self.parsed_data[-1].substitute
            ):
                # We have switched to substitutes for the current candidacy
                self.__add_candidate(content, order)
                self.candidate_order = order
            else:
                # We have switched to a new candidacy
                self.__set_candidacy(content)

    def __set_candidacy(self, content: str) -> None:
        """Extracts and sets the current candidacy."""
        if len(self.parsed_data) == 0 and self.current_candidacy is not None:
            raise ValueError("Candidacy set before any candidates were parsed.")
        self.__mark_candidacy_as_finished()
        current_party, current_acronym = _extract_candidacy(content)
        self.current_candidacy = Candidacy(name=current_party, acronym=current_acronym)
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
            if self.current_candidacy.name.endswith("-"):
                full_content = self.current_candidacy.name[:-1] + line
            else:
                full_content = self.current_candidacy.name + " " + line
            new_name, new_acronym = _extract_candidacy(full_content)
            self.current_candidacy = replace(
                self.current_candidacy, name=new_name, acronym=new_acronym
            )

    def __validate_substitutes_count(self) -> int:
        """Validates that the number of substitutes matches the expected count for the previous candidacy."""
        expected_substitutes = 0
        for c in self.parsed_data[::-1]:
            if c.candidacy == self.current_candidacy and c.substitute:
                expected_substitutes += 1
            else:
                break
        if (
            self.expected_substitutes is not None
            and expected_substitutes != self.expected_substitutes
        ):
            raise ValueError(
                f"Mismatch in expected substitutes for {self.current_candidacy.name}: "
                f"expected {self.expected_substitutes}, found {expected_substitutes}"
            )
        return expected_substitutes

    def __validate_candidates_count(self) -> None:
        """Validates that the number of candidates matches the expected count for the previous candidacy."""
        expected_candidates = 0
        previous_candidacy = None
        for c in self.parsed_data[::-1]:
            if c.candidacy == self.current_candidacy:
                expected_candidates += 1
            else:
                previous_candidacy = c.candidacy
                previous_province = c.province
                break
        if expected_candidates == 0:
            raise ValueError(
                f"No candidates found for {self.current_candidacy.name} in {self.current_province}"
            )
        # Calculate the candidates of the previous candidacy to compare with the current one
        if previous_candidacy is None:
            return  # No previous candidacy to compare with
        if previous_province != self.current_province:
            return # Different province, no need to compare
        previous_candidates = 0
        for c in self.parsed_data[-expected_candidates-1::-1]:
            if c.candidacy == previous_candidacy:
                previous_candidates += 1
            elif c.candidacy != previous_candidacy:
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
        self.expected_substitutes = self.__validate_substitutes_count()
        # In some cases, the substitutes are not explicitly marked
        if self.expected_substitutes == 0:
            self.expected_substitutes = None
        self.__validate_candidates_count()
        self.current_candidacy = None
        self.candidate_order = 0
        self.pending_order = None
        self.is_substitute = False
