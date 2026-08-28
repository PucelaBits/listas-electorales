import logging
import os

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
        with requests.get(url, headers=headers, stream=True, timeout=60, **kwargs) as response:
            if response.status_code == 200:
                # Write to disk in 8KB chunks to reduce memory usage
                with open(cache_path, "wb") as f:
                    f.writelines(response.iter_content(chunk_size=8192))
                return

        raise FileNotFoundError(
            f"Failed to download file from {url}. Status code: {response.status_code}"
        )
