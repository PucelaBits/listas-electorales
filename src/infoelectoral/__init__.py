import os

from common import CACHE_DIR, CachedRequester
from common.models import Election, ElectionType
from infoelectoral.download import extract_dat_files, generate_url_filename
from infoelectoral.parse import DATElectionParser


def load_election(election_type: ElectionType, year: int, month: int) -> Election:
    """
    Downloads and parses the election data for the specified election type, year, and month.
    Returns an Election object containing the parsed data.
    """
    filename, url = generate_url_filename(election_type, year, month)
    # Download the zip file from the generated URL
    cache_path = os.path.join(CACHE_DIR, "infoelectoral", filename)
    CachedRequester.get(url, cache_path, verify=False)

    # Extract the DAT files
    candidacy_dat_filepath, candidate_dat_filepath = extract_dat_files(
        cache_path, year, month, election_type
    )

    # Parse the DAT files to create an Election object
    election = DATElectionParser(candidacy_dat_filepath, candidate_dat_filepath).parse()
    return election
