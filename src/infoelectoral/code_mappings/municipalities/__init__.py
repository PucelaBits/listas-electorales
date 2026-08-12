from .ine import load_ine_municipalities_mapping
from .missing import MISSING_MUNICIPIOS


def load_municipalities_mapping(years: list[int]) -> dict[str, str | None]:
    ine_mapping = load_ine_municipalities_mapping(years)
    return {**ine_mapping, **MISSING_MUNICIPIOS}
