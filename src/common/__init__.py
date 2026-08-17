import logging
import os
import re

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CACHE_DIR = os.environ.get("CACHE_FOLDER", ".cache")


class CachedRequester:
    """
    A helper class to manage HTTP requests and local file caching.
    """

    @classmethod
    def get(cls, url: str, cache_path: str, **kwargs) -> None:
        """
        Downloads and streams the file to disk in chunks if it isn't cached.
        """
        # If it's already cached, just return a read-only file stream
        if os.path.exists(cache_path):
            logger.debug(f"Using cached file for {url} at {cache_path}")
            return

        # Create the folder if it doesn't exist
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        # If not cached, request the file with stream=True
        headers = {"User-Agent": "ListaCandidatosElectorales/1.0"}

        # Using a context manager ensures the network connection is closed properly
        logger.debug(f"Downloading file for {url} to {cache_path}")
        with requests.get(url, headers=headers, stream=True, **kwargs) as response:
            if response.status_code == 200:
                # Write to disk in 8KB chunks to reduce memory usage
                with open(cache_path, "wb") as f:
                    f.writelines(response.iter_content(chunk_size=8192))
                return

        raise FileNotFoundError(
            f"Failed to download file from {url}. Status code: {response.status_code}"
        )


def prettify_name(name: str | None) -> str | None:
    """
    Cleans and formats a candidate's full name.

    Adapted from "infoelectoral" project by Jaime Gómez-Obregón (AGPL-3.0 license).

    @copyright     Copyright (c) Jaime Gómez-Obregón
    @link          https://github.com/JaimeObregon/infoelectoral
    @license       https://www.gnu.org/licenses/agpl-3.0.en.html
    """
    if name is None:
        return None
    name = name.strip()
    if not name:
        return None

    # Title casing
    name = name.title()

    # Replacements map
    replacements = {
        r"\bDe Los\b": "de los",
        r"\bDe Las\b": "de las",
        r"\bDe La\b": "de la",
        r"\bDel\b": "del",
        r"\bAl\b": "al",
        r"\bDe\b": "de",
        r"\bY\b": "y",
        r"\bI\b": "i",
        r"\bE\b": "e",
        r"\bEl\b": "el",
        r"\bLa\b": "la",
        r"\bLos\b": "los",
        r"\bLas\b": "las",
        r"\bDa\b": "da",
        r"\bDos\b": "dos",
        r"\bDi\b": "di",
        r"\bVon\b": "von",
        r"\bVan\b": "van",
        r"\bM[ªa]\b|\bM\.?[ªa]\.?\b": "María",  # Mª, M.ª, Ma., Ma, etc.
        r"\bFco\.?\b|\bF\.co\b": "Francisco",
    }

    for pattern, replacement in replacements.items():
        name = re.sub(pattern, replacement, name)

    # Remove suffixes inside parentheses
    name = re.sub(r"\(.+\)\s*$", "", name).strip()

    return name if name else None


def prettify_municipality(name: str) -> str:
    """
    Beautifies municipality names, handling double spaces and suffixes.
    Adapted from "infoelectoral" project by Jaime Gómez-Obregón (AGPL-3.0 license).

    @copyright     Copyright (c) Jaime Gómez-Obregón
    @link          https://github.com/JaimeObregon/infoelectoral
    @license       https://www.gnu.org/licenses/agpl-3.0.en.html
    """
    name = re.sub(r" {2,}", " ", name).strip()

    parts = name.split("/")
    formatted_parts = []

    suffix_pattern = (
        r"^(.+), (A|As|El|Els|Es|L'|La|Las|Les|Los|O|Os|Sa|Ses|el|els|l'|la|les)$"
    )

    for part in parts:
        part = re.sub(suffix_pattern, r"\2 \1", part)
        part = re.sub(r"^[Ll]' ", "L'", part)
        part = part[0].upper() + part[1:] if part else part
        formatted_parts.append(part)

    return "/".join(formatted_parts)
