import os

import pandas as pd

from common import CACHE_DIR, CachedRequester, logger


def get_ine_municipality_codes(year: int) -> dict[str, str]:
    yy = str(year)[-2:]
    extensions = [".xlsx", ".xls"]

    file_path = None
    for ext in extensions:
        if year > 2020:
            url = f"https://www.ine.es/daco/daco42/codmun/diccionario{yy}.xlsx"
        else:
            url = f"https://www.ine.es/daco/daco42/codmun/codmun{yy}/{yy}codmun{ext}"
        cache_path = os.path.join(CACHE_DIR, "ine-municipalities", f"{year}codmun{ext}")
        try:
            CachedRequester.get(url, cache_path)
            file_path = cache_path
            break
        except Exception as e:  # noqa: BLE001
            logger.debug(
                f"Failed to retrieve INE municipality codes for year {year} with extension {ext}.\nError details: {e}"
            )
            continue

    # Handle unexpected cases where the file isn't found
    if not file_path:
        raise FileNotFoundError(
            f"Unable to retrieve INE municipality codes for year {year}"
        )

    df = pd.read_excel(file_path, dtype=str)
    if "CPRO" not in df.columns:
        df = pd.read_excel(file_path, dtype=str, skiprows=1)
    if "CPRO" not in df.columns:
        raise ValueError(
            f"Unexpected format for INE municipality codes file for year {year}. 'CPRO' column not found: {df.columns.tolist()}"
        )
    # Clean the column names
    df.columns = [col.upper().strip() for col in df.columns]
    df["INE_CODE"] = df["CPRO"].str.zfill(2) + df["CMUN"].str.zfill(3)
    # We only want the last 5 digits of the INE code, which represent the province + municipality code
    filtered_ine_code = df["INE_CODE"].str[-5:]

    return dict(zip(filtered_ine_code, df["NOMBRE"]))
