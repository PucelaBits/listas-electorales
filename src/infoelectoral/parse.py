from common import build_full_name, prettify_municipality, prettify_name
from common.models import Candidacy, Candidate, Election, ElectionType

from .code_mappings.mappings import PROVINCES
from .code_mappings.municipalities import MunicipalityMapper
from .dat_files import CandidacyDATParser, CandidateDATParser


class DATElectionParser:
    def __init__(self, candidacy_dat_filepath: str, candidate_dat_filepath: str):
        self.municipality_mapper = MunicipalityMapper.instance()
        self.candidacy_parser = CandidacyDATParser(candidacy_dat_filepath)
        self.candidate_parser = CandidateDATParser(candidate_dat_filepath)

    def parse(self) -> Election:
        dat_candidacies = {c.code: c for c in self.candidacy_parser.parse()}
        candidacies = {
            c.code: Candidacy(acronym=c.acronym, name=c.name)
            for c in dat_candidacies.values()
        }

        elections = {}

        for dat_candidate in self.candidate_parser.parse():
            if dat_candidate.candidacy_code not in candidacies:
                raise ValueError(
                    f"Candidacy code {dat_candidate.candidacy_code} not found for candidate {dat_candidate.nombre}."
                )
            dat_candidacy_code = dat_candidate.candidacy_code
            candidacy = candidacies[dat_candidacy_code]
            dat_candidacy = dat_candidacies[dat_candidacy_code]

            province = None
            municipality = None
            if dat_candidate.province_code:
                province = PROVINCES.get(dat_candidate.province_code, None)
                municipality_full_code = (
                    dat_candidate.province_code + dat_candidate.municipality_code
                )
                municipality = self.municipality_mapper.get_municipalities_mapping(
                    dat_candidacy.year
                ).get(municipality_full_code, None)
                if municipality is not None:
                    municipality = prettify_municipality(municipality)

            candidate = Candidate(
                candidacy=candidacy,
                order=dat_candidate.order,
                full_name=prettify_name(
                    build_full_name(
                        first_name=dat_candidate.name,
                        last_name1=dat_candidate.first_surname,
                        last_name2=dat_candidate.second_surname,
                    )
                ),
                sex=dat_candidate.sex,
                elected=dat_candidate.elected,
                substitute=dat_candidate.substitute,
                province=province,
                municipality=municipality,
            )
            elections.setdefault(
                (
                    dat_candidacy.election_type,
                    dat_candidacy.year,
                    dat_candidacy.month,
                    dat_candidate.repetition,
                ),
                [],
            ).append(candidate)

        if len(elections) == 0:
            raise ValueError(f"No elections found in the provided DAT files: {self.candidacy_parser.filepath} and {self.candidate_parser.filepath}")

        if len(elections) > 1:
            raise ValueError(
                f"Multiple elections found in the provided DAT files. {len(elections)} elections detected. "
                "Please ensure that the files correspond to a single election."
            )

        (election_type, year, month, repetition), candidates = next(
            iter(elections.items())
        )
        return Election(
            year=year,
            month=month,
            repetition=repetition,
            type=ElectionType(election_type),
            candidates=tuple(candidates),
        )
