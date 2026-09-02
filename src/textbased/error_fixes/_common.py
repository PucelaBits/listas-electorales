import re
from collections.abc import Callable

ERROR_FIXERS: dict[tuple[str, int, int], Callable[[str], str]] = {}


def register_fixer(region: str, year: int, month: int):
    """Decorator to register a text-fixing function for a specific batch."""

    def decorator(func: Callable[[str], str]):
        ERROR_FIXERS[(region, year, month)] = func
        return func

    return decorator


def clean_ocr_text(text: str) -> str:
    """Cleans up common OCR errors in the text, such as stray punctuation, missing dots after numbers, and inconsistent formatting."""
    # Clean up "Núm" variations (e.g., "Núm.-", "Núm.- ", "Núm ")
    text = re.sub(r"Núm[\.\-\s]+", "Núm. ", text)

    # Remove stray quotes around numbers and dots
    text = re.sub(r"['´`\"](?=\d)", "", text)
    text = re.sub(r"(?<=\d)['´`\"]", "", text)
    text = re.sub(r"(?<=\d\.)['´`\"]", "", text)

    # Fix SINGLE colons and exclamation marks after numbers (e.g., "11:" -> "11.")
    text = re.sub(r"\b(\d+)[:!•]", r"\1.", text)

    # Fix CLUSTERS of messy punctuation (dots, dashes, commas, colons, exclamation marks)
    text = re.sub(r"\b(\d+)[\.\-\,:\!•]{2,}\s*", r"\1. ", text)

    # Fix stray dots before list numbers (e.g., ".13." -> "13.")
    text = re.sub(r"(?<=\s)[\.,](\d+)[\.,]", r"\1.", text)

    # Add missing dots after numbers preceding names/entities (e.g., "10 Don" -> "10. Don")
    text = re.sub(r"\b(\d+)\ +(?=Don|Doña|[A-Z]{2,})", r"\1. ", text)

    # Fix commas separating titles (e.g., "Don,Juan" -> "Don Juan")
    text = re.sub(r"(Don|Doña)[,|-]", r"\1 ", text)

    # Remove stray single letters surrounded by dots after numbers (e.g., "3.x. " -> "3. ")
    text = re.sub(r"\b(\d+)\.[a-zA-Z]\.\s*", r"\1. ", text)

    return text
