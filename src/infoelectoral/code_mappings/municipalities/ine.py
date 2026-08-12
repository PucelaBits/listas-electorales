import os

import pandas as pd

from helper_utils import CachedRequester, logger


def load_ine_municipalities_mapping(years: list[int]) -> dict[str, str]:
    mapping = {}
    for year in years:
        try:
            mapping.update(get_municipality_codes(year))
        except Exception as e:  # noqa: BLE001
            logger.warning(f"Failed to load INE municipality codes for year {year}. Error details: {e}")
            continue
    if len(mapping) == 0:
        raise ValueError("No valid INE municipality codes could be loaded for the provided years.")
    return mapping


def get_municipality_codes(year: int) -> dict[str, str]:
    requester = CachedRequester()
    yy = str(year)[-2:]
    extensions = [".xlsx", ".xls"]

    file_buffer = None
    for ext in extensions:
        url = f"https://www.ine.es/daco/daco42/codmun/codmun{yy}/{yy}codmun{ext}"
        filepath = os.path.join("ine-municipalities", f"{year}codmun{ext}")
        try:
            file_buffer = requester.get(url, filepath)
            break
        except Exception as e:  # noqa: BLE001
            logger.debug(f"Failed to retrieve INE municipality codes for year {year} with extension {ext}.\nError details: {e}")
            continue

    # Handle unexpected cases where the file isn't found
    if not file_buffer:
        raise FileNotFoundError(
            f"Unable to retrieve INE municipality codes for year {year}"
        )

    with file_buffer as f:
        df = pd.read_excel(f, dtype=str)
        if 'CPRO' not in df.columns:
            df = pd.read_excel(f, dtype=str, skiprows=1)
        # Clean the column names
        df.columns = [col.upper().strip() for col in df.columns]
        df["INE_CODE"] = df["CPRO"].str.zfill(2) + df["CMUN"].str.zfill(3)
        # We only want the last 5 digits of the INE code, which represent the province + municipality code
        filtered_ine_code = df["INE_CODE"].str[-5:]

        return dict(zip(filtered_ine_code, df["NOMBRE"]))
    raise OSError(f"Error reading file for INE municipality codes for year {year}")
