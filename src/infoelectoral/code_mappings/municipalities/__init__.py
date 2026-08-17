from datetime import datetime
from zoneinfo import ZoneInfo

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
        year = max(MIN_INE_YEAR, min(year, MAX_INE_YEAR))
        ine_mapping = get_ine_municipality_codes(year)
        return {**MISSING_MUNICIPIOS, **ine_mapping}
