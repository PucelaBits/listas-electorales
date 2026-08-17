import argparse
import csv
import logging
import os
from collections.abc import Generator
from dataclasses import dataclass

import pandas as pd
from compression import gzip

from common import logger
from common.models import ElectionType
from infoelectoral import load_election as infoelectoral_load_election


@dataclass(frozen=True)
class ElectionData:
    election_type: ElectionType
    region: str | None
    year: int
    month: int


def read_election_data(file_path: str) -> Generator[ElectionData]:
    """
    Reads election data from a CSV file and returns it as a pandas DataFrame.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Election data file not found: {file_path}")

    df = pd.read_csv(file_path)
    # Sort by year and month to ensure chronological order
    df.sort_values(by=["year", "month"], inplace=True)
    for _, row in df.iterrows():
        if row["election_type"] == "europeas":
            if row["year"] == 1985 and row["month"] == 12:
                # Missing data for European elections, skipping these entries
                logger.warning(
                    f"Skipping {row['year']} European elections due to missing data in the source."
                )
                continue
            yield ElectionData(
                ElectionType.PARLAMENTO_EUROPEO,
                None,
                int(row["year"]),
                int(row["month"]),
            )
        elif row["election_type"] == "municipales":
            if (row["year"] == 1979 and row["month"] == 4) or (
                row["year"] == 1983 and row["month"] == 5
            ):
                # Missing data for municipal elections, skipping this entry
                logger.warning(
                    f"Skipping {row['year']} municipal elections due to missing data in the source."
                )
                continue
            yield ElectionData(
                ElectionType.MUNICIPALES, None, int(row["year"]), int(row["month"])
            )
        elif row["election_type"] == "autonomicas":
            # TODO
            yield ElectionData(
                ElectionType.AUTONOMICAS,
                row["scope"],
                int(row["year"]),
                int(row["month"]),
            )
        elif row["election_type"] == "generales":
            yield ElectionData(
                ElectionType.CONGRESO, None, int(row["year"]), int(row["month"])
            )
            yield ElectionData(
                ElectionType.SENADO, None, int(row["year"]), int(row["month"])
            )
        else:
            raise ValueError(f"Unknown election type: {row['election_type']}")


def main(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if args.output_file.endswith(".gz"):
        logger.info(f"Output will be written to compressed file: {args.output_file}")
    else:
        logger.info(f"Output will be written to file: {args.output_file}")
    with (
        gzip.open(args.output_file, mode="wt", newline="", encoding="utf-8")
        if args.output_file.endswith(".gz")
        else open(args.output_file, mode="wt", newline="", encoding="utf-8") as f
    ):
        writer = csv.writer(f)
        # Write header
        writer.writerow(
            [
                "full_name",
                "election_type",
                "year",
                "month",
                "acronym",
                "name",
                "municipality",
                "province",
                "order",
                "substitute",
                "elected",
            ]
        )

        for election_data in read_election_data(args.election_file):
            logger.info(
                f"Processing election: {election_data.election_type.value} "
                f"{election_data.year}-{election_data.month}"
            )

            if election_data.region is None:
                election = infoelectoral_load_election(
                    election_data.election_type, election_data.year, election_data.month
                )
                for candidate in election.candidates:
                    name = candidate.full_name if candidate.full_name else ""
                    municipality = (
                        candidate.municipality if candidate.municipality else ""
                    )
                    province = candidate.province if candidate.province else ""
                    substitute = "1" if candidate.substitute else "0"
                    elected = "1" if candidate.elected else "0"
                    writer.writerow(
                        [
                            name,
                            election.type.value,
                            election.year,
                            election.month,
                            candidate.candidacy.acronym,
                            candidate.candidacy.name,
                            municipality,
                            province,
                            candidate.order,
                            substitute,
                            elected,
                        ]
                    )


if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(description="ListaCandidatosElectorales")
    arg_parser.add_argument(
        "--election_file",
        type=str,
        help="Path to the election data CSV file",
        default=os.path.join(
            os.path.dirname(__file__), "..", "data", "election_dates.csv"
        ),
    )
    arg_parser.add_argument(
        "--output_file",
        type=str,
        help="Path to the output CSV(.GZ) file",
        default=os.path.join(
            os.path.dirname(__file__), "..", "data", "output_data.csv.gz"
        ),
    )
    arg_parser.add_argument("--debug", action="store_true", help="Enable debug logging")

    main(arg_parser.parse_args())
