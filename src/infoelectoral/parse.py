from common import logger
from common.models import Candidacy, Candidate, Election, ElectionType
from common.names import prettify_municipality, prettify_name

from .code_mappings.mappings import PROVINCES
from .code_mappings.municipalities import MAX_INE_YEAR, MIN_INE_YEAR, MunicipalityMapper
from .dat_files import CandidacyDATParser, CandidateDATParser


class DATElectionParser:
    def __init__(self, candidacy_dat_filepath: str, candidate_dat_filepath: str):
        self.municipality_mapper = MunicipalityMapper.instance()
        self.candidacy_parser = CandidacyDATParser(candidacy_dat_filepath)
        self.candidate_parser = CandidateDATParser(candidate_dat_filepath)

    def parse(self) -> Election:
        candidacies = {
            c.code: Candidacy(acronym=c.acronym, name=c.name)
            for c in self.candidacy_parser.parse()
        }

        elections = {}

        for dat_candidate in self.candidate_parser.parse():
            if dat_candidate.candidacy_code not in candidacies:
                raise ValueError(
                    f"Candidacy code {dat_candidate.candidacy_code} not found for candidate {dat_candidate.nombre}."
                )
            dat_candidacy_code = dat_candidate.candidacy_code
            candidacy = candidacies[dat_candidacy_code]

            province = None
            municipality = None
            if (
                dat_candidate.province_code is not None
                and dat_candidate.municipality_code is not None
            ):
                province = PROVINCES.get(dat_candidate.province_code, None)
                municipality_full_code = (
                    dat_candidate.province_code + dat_candidate.municipality_code
                )
                if municipality_full_code.startswith("51"):
                    municipality = "Ceuta"
                elif municipality_full_code.startswith("52"):
                    municipality = "Melilla"
                else:
                    municipality = self.municipality_mapper.get_municipalities_mapping(
                        dat_candidate.year
                    ).get(municipality_full_code, "N/A")
                if municipality == "N/A" and (
                    dat_candidate.year >= MIN_INE_YEAR
                    and dat_candidate.year <= MAX_INE_YEAR
                ):
                    logger.warning(
                        f"Municipality code {municipality_full_code} ({province}) not found for candidate {dat_candidate.full_name} in year {dat_candidate.year}."
                    )
                elif municipality is not None:
                    municipality = prettify_municipality(municipality)

            candidate = Candidate(
                candidacy=candidacy,
                order=dat_candidate.order,
                full_name=prettify_name(dat_candidate.full_name),
                sex=dat_candidate.sex,
                elected=dat_candidate.elected,
                substitute=dat_candidate.substitute,
                province=province,
                municipality=municipality,
            )
            elections.setdefault(
                (
                    dat_candidate.election_type,
                    dat_candidate.year,
                    dat_candidate.month,
                ),
                [],
            ).append(candidate)

        if len(elections) == 0:
            raise ValueError(
                f"No elections found in the provided DAT files: {self.candidacy_parser.filepath} and {self.candidate_parser.filepath}"
            )

        if len(elections) > 1:
            raise ValueError(
                f"Multiple elections found in the provided DAT files. {len(elections)} elections detected. "
                "Please ensure that the files correspond to a single election."
            )

        (election_type, year, month), candidates = next(
            iter(elections.items())
        )
        return Election(
            year=year,
            month=month,
            type=ElectionType(election_type),
            candidates=tuple(candidates),
        )
