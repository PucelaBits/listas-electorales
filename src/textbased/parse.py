import glob
import re
from collections.abc import Generator
from dataclasses import replace

import pymupdf

from common import logger
from common.models import Candidacy, Candidate
from common.names import prettify_name

from .error_fixes import ERROR_FIXERS

LONG_LINE_THRESHOLD = 150  # Arbitrary threshold for splitting long lines

# Extract candidacy name and acronym from the clean content
_CANDIDACY_RE = re.compile(r"^(.*?)\s*\((.*?)\)$")


def _extract_candidacy(content: str) -> tuple[str, str]:
    acr_match = _CANDIDACY_RE.search(content)
    if acr_match:
        current_party = acr_match.group(1).strip()
        current_acronym = acr_match.group(2).strip()
    else:
        current_party = content.strip()
        current_acronym = ""
    return current_party, current_acronym


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
        or "octubre" in line_lower
        or "noviembre" in line_lower
        or "diciembre" in line_lower
    )


class TextReader:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = ERROR_FIXERS.get((region, year, month), None)

    def parse(self) -> Generator[str, None, None]:
        pdf_files = glob.glob(f"{self.folderpath}/candidaturas*.pdf")
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.folderpath}")

        for pdf_path in pdf_files:
            yield from self.__parse_single_file(pdf_path)

    def __parse_single_file(self, pdf_path: str) -> Generator[str, None, None]:
        doc = pymupdf.open(pdf_path)
        for page in doc:
            text = page.get_text(sort=True)
            if not text:
                continue

            if self.fix_text is not None:
                text = self.fix_text(text)

            for line in text.split("\n"):
                line = line.strip()
                if not line:
                    continue
                # If the line is too long, it might have multiple stuff inside, split it
                if len(line) > LONG_LINE_THRESHOLD:
                    # Make a best-effort split using spaces
                    for range_start in range(0, len(line), LONG_LINE_THRESHOLD):
                        selected_line = line[
                            range_start : range_start + LONG_LINE_THRESHOLD
                        ].strip()
                        if selected_line:
                            yield selected_line
                else:
                    yield line


class TextElectionParser:
    PROVINCE_RE = re.compile(
        r"(?:JUNTA ELECTORAL\s+PROVINCIAL\s+DE\s+|CIRCUNSCRIPCI[ÓO]N\s+ELECTORAL\:\s+)([A-ZÁÉÍÓÚÑ\s]+)",
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

    def __init__(self, text_reader: TextReader):
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
        counts_by_province = {}

        for candidate in self.parsed_data:
            prov = candidate.province
            cand = candidate.candidacy

            if prov not in counts_by_province:
                counts_by_province[prov] = {}
            if cand not in counts_by_province[prov]:
                counts_by_province[prov][cand] = 0

            counts_by_province[prov][cand] += 1

        # Validate that all candidacies have the same number of candidates FOR EACH province
        for province, candidacy_counts in counts_by_province.items():
            if len(set(candidacy_counts.values())) > 1:
                # Find the mismatch for this specific province
                reference_count = next(iter(candidacy_counts.values()))
                mismatch = {
                    candidacy.name: count
                    for candidacy, count in candidacy_counts.items()
                    if count != reference_count
                }

                # Safely extract province name (in case 'province' is an object rather than a string)
                prov_name = getattr(province, "name", province)

                raise ValueError(
                    f"Mismatch in number of candidates across candidacies in province '{prov_name}': {mismatch}"
                )

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
            # Change of province indicates a new candidacy section, so reset candidacy and candidate order
            self.current_candidacy = None
            self.candidate_order = 0
            self.pending_order = None
            self.expected_substitutes = None
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
            self.current_candidacy = None
            self.candidate_order = 0
            self.pending_order = None
            self.is_substitute = False
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
        if not re.search(r"\d", line) and "núm." not in line.lower() and not self.line_completed:
            self.__handle_unmatched_line(line)
            return
        # Mark the line as completed to avoid adding more stuff to the last candidate
        self.line_completed = True

    def __handle_numbered_item(self, order: int, content: str) -> None:
        """Processes lines that start with a number (either a candidacy or a candidate)."""
        if "disposiciones generales" in content.lower():
            # Skip lines that are part of the general provisions section
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
        current_party, current_acronym = _extract_candidacy(content)
        # Validate the number of substitutes for the previous candidacy before switching
        if self.current_candidacy is not None:
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
            self.expected_substitutes = expected_substitutes
            # In some cases, the substitutes are not explicitly marked
            if self.expected_substitutes == 0:
                self.expected_substitutes = None
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
        # Remove digits from the name
        content = re.sub(r"\d", "", content).strip()
        candidate = Candidate(
            full_name=prettify_name(content.rstrip(".")),
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
            # Remove all digits from the text
            line = re.sub(r"\d", "", line).strip()
            self.parsed_data[-1] = replace(
                self.parsed_data[-1],
                full_name=prettify_name(
                    self.parsed_data[-1].full_name + " " + line.rstrip(".")
                ),
            )
        elif self.current_candidacy and self.candidate_order == 0:
            # If we are not currently parsing candidates, this line is a continuation of the candidacy name
            new_name, new_acronym = _extract_candidacy(
                self.current_candidacy.name + " " + line
            )
            self.current_candidacy = replace(
                self.current_candidacy, name=new_name, acronym=new_acronym
            )
