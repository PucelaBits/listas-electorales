from datetime import datetime
from zoneinfo import ZoneInfo

from common import logger

from .ine import get_ine_municipality_codes
from .missing import MISSING_MUNICIPIOS

MIN_INE_YEAR = 2001
MAX_INE_YEAR = datetime.now(tz=ZoneInfo("Europe/Madrid")).year


class MunicipalityMapper:
    _instance = None
    """Singleton class to manage the mapping of municipality codes to names."""

    def __init__(self):
        if MunicipalityMapper._instance is not None:
            raise RuntimeError(
                "Use MunicipalityMapper.instance() to get the singleton instance."
            )
        self._cache: dict[int, dict[str, str | None]] = {}

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def get_municipalities_mapping(self, year: int) -> dict[str, str | None]:
        if year not in self._cache:
            self._cache[year] = self.load_municipalities_mapping(year)
        return self._cache[year]

    def load_municipalities_mapping(self, year: int) -> dict[str, str | None]:
        # Ensure the year is not earlier than 2003 and than the current year
        year = max(MIN_INE_YEAR, min(year, MAX_INE_YEAR))
        # Explore years around the given year to find a valid INE mapping
        for i in range(MAX_INE_YEAR - MIN_INE_YEAR):
            if year + i > MAX_INE_YEAR and year - i < MIN_INE_YEAR:
                break
            for y in (year + i, year - i):
                if y < MIN_INE_YEAR or y > MAX_INE_YEAR:
                    continue
                try:
                    ine_mapping = get_ine_municipality_codes(y)
                    return {**ine_mapping, **MISSING_MUNICIPIOS}
                except FileNotFoundError as e:
                    logger.warning(
                        f"Failed to load INE municipality codes for year {y}. Error details: {e}"
                    )
                    continue
        raise ValueError(f"No valid INE municipality codes could be loaded for {year}")
