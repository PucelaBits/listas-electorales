import os

from common.models import Election, ElectionType

from .parse import TextElectionParser, TextReader

TEXT_BASED_DATA_DIR = os.path.join(
    os.path.dirname(__file__), "..", "..", "data", "regions"
)


def load_election(
    election_type: ElectionType, region: str, year: int, month: int
) -> Election:
    """
    Loads and parses the election data for the specified region, year, and month.
    Returns an Election object containing the parsed data.
    """
    # Construct the file path for the text-based election data
    folderpath = os.path.join(TEXT_BASED_DATA_DIR, region, f"{year:04d}_{month:02d}")

    # Parse the text-based election data to create an Election object
    text_reader = TextReader(folderpath, region, year, month)
    try:
        parser = TextElectionParser(text_reader)
        parser.parse()
        candidates = parser.build()
    except Exception as e:
        raise RuntimeError(
            f"Failed to parse election data for {region} {year}-{month}: {e}"
        ) from e
    return Election(
        year=year,
        month=month,
        candidates=candidates,
        type=election_type,
    )
