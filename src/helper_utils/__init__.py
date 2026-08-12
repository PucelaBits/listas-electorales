import logging
import os
import re
from typing import BinaryIO

import requests

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CachedRequester:
    """
    A helper class to manage HTTP requests and local file caching.
    Streams downloads to disk and returns a file-like buffer to save memory.
    """

    def __init__(self):
        self.cache_dir = os.environ.get("CACHE_FOLDER", ".cache")
        os.makedirs(self.cache_dir, exist_ok=True)

    def get(self, url: str, filepath: str) -> BinaryIO:
        """
        Returns an open, readable file buffer.
        Downloads and streams the file to disk in chunks if it isn't cached.
        """
        cache_path = os.path.join(self.cache_dir, filepath)

        # If it's already cached, just return a read-only file stream
        if os.path.exists(cache_path):
            logger.debug(f"Using cached file for {url} at {cache_path}")
            return open(cache_path, "rb")

        # Create the folder if it doesn't exist
        os.makedirs(os.path.dirname(cache_path), exist_ok=True)

        # If not cached, request the file with stream=True
        headers = {"User-Agent": "ListaCandidatosElectorales/1.0"}

        # Using a context manager ensures the network connection is closed properly
        logger.debug(f"Downloading file for {url} to {cache_path}")
        with requests.get(url, headers=headers, stream=True) as response:
            if response.status_code == 200:
                # Write to disk in 8KB chunks to reduce memory usage
                with open(cache_path, "wb") as f:
                    f.writelines(response.iter_content(chunk_size=8192))

                # Now that it is safely on disk, return a read-only stream
                return open(cache_path, "rb")

        raise FileNotFoundError(
            f"Failed to download file from {url}. Status code: {response.status_code}"
        )


def prettify_name(name: str) -> str | None:
    """
    Cleans and formats a candidate's full name.
    """
    if not name or not name.strip():
        return None

    # Title casing
    name = name.title()

    # Replacements map for particles
    replacements = {
        r" De Los ": " de los ",
        r" De La ": " de la ",
        r" Del ": " del ",
        r" De ": " de ",
        r" Y ": " y ",
        r" I ": " i ",
        r" E ": " e ",
    }

    for pattern, replacement in replacements.items():
        name = re.sub(pattern, replacement, name)

    # Remove suffixes inside parentheses
    name = re.sub(r"\(.+\)\s*$", "", name).strip()

    return name if name else None


def prettify_municipality(name: str) -> str:
    """
    Beautifies municipality names, handling double spaces and suffixes.
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
