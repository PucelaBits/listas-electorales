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
    # This will turn "11.:", "1.-.", "10!.", etc., into a clean "11. "
    text = re.sub(r"\b(\d+)[\.\-\,:\!•]{2,}\s*", r"\1. ", text)

    # Fix stray dots before list numbers (e.g., ".13." -> "13.")
    text = re.sub(r"(?<=\s)[\.,](\d+)[\.,]", r"\1.", text)

    # Add missing dots after numbers preceding names/entities (e.g., "10 Don" -> "10. Don")
    # Looks for a number followed by a space, then "Don", "Doña", or an uppercase word.
    text = re.sub(r"\b(\d+)\s+(?=Don|Doña|[A-Z]{2,})", r"\1. ", text)

    # Fix commas separating titles (e.g., "Don,Juan" -> "Don Juan")
    text = re.sub(r"(Don|Doña)[,|-]", r"\1 ", text)
    return text
