import os
import re
import zipfile

from common import CACHE_DIR
from common.models import ElectionType

from .code_mappings.mappings import ELECTION_TYPES

INVERSE_ELECTION_TYPES = {v: k for k, v in ELECTION_TYPES.items()}


def generate_url_filename(election_type: ElectionType, year: int, month: int) -> str:
    """
    Generates the download URL for the election zip file based on the provided parameters.
    """
    base_url = "https://infoelectoral.interior.gob.es/estaticos/docxl/apliextr/"
    election_type_str = INVERSE_ELECTION_TYPES.get(election_type, None)
    assert election_type_str is not None, (
        f"Election type {election_type} is not recognized."
    )
    filename = f"{election_type_str}{year}{month:02d}_MUNI.zip"
    return filename, base_url + filename


def extract_dat_files(
    zip_path: str, year: int, month: int, election_type: ElectionType
) -> tuple[str, str]:
    """
    Extracts the required DAT files (03*.DAT and 04*.DAT) from a zip file.
    Returns a tuple containing the paths to the candidacy and candidate DAT files.
    """
    # Extract to a directory specifically for this election
    zip_basename = os.path.splitext(os.path.basename(zip_path))[0]
    extract_dir = os.path.join(
        CACHE_DIR,
        "infoelectoral",
        f"{zip_basename}_{year}_{month:02d}_{election_type.value}",
    )
    os.makedirs(extract_dir, exist_ok=True)

    # Check if files are already extracted using pattern matching in the directory
    candidacy_files_in_dir = [
        f for f in os.listdir(extract_dir) if re.match(r"03.*\.DAT$", f)
    ]
    candidate_files_in_dir = [
        f for f in os.listdir(extract_dir) if re.match(r"04.*\.DAT$", f)
    ]

    if candidacy_files_in_dir and candidate_files_in_dir:
        return (
            os.path.join(extract_dir, candidacy_files_in_dir[0]),
            os.path.join(extract_dir, candidate_files_in_dir[0]),
        )

    with zipfile.ZipFile(zip_path, "r") as z:
        # Find files matching patterns
        candidacy_files = [f for f in z.namelist() if re.match(r"03.*\.DAT$", f)]
        candidate_files = [f for f in z.namelist() if re.match(r"04.*\.DAT$", f)]

        if not candidacy_files or not candidate_files:
            raise ValueError(
                f"Could not find required DAT files in {os.path.basename(zip_path)}"
            )

        # Use the first match for each type
        candidacy_dat_filepath = os.path.join(extract_dir, candidacy_files[0])
        candidate_dat_filepath = os.path.join(extract_dir, candidate_files[0])

        # Extract the files
        z.extractall(extract_dir)

        return candidacy_dat_filepath, candidate_dat_filepath
