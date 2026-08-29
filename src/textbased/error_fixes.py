import glob
import re
from collections.abc import Callable, Generator

import fitz

_ERROR_FIXERS: dict[tuple[str, int, int], Callable[[str], str]] = {}


def register_fixer(region: str, year: int, month: int):
    """Decorator to register a text-fixing function for a specific batch."""

    def decorator(func: Callable[[str], str]):
        _ERROR_FIXERS[(region, year, month)] = func
        return func

    return decorator


@register_fixer("castilla_y_leon", 1983, 5)
def fix_cyl_1983_05(text: str) -> str:
    return re.sub(
        r"^COALICION PCOE-PCEU", "3. COALICION PCOE-PCEU", text, flags=re.MULTILINE
    )


class TextParser:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = _ERROR_FIXERS.get((region, year, month), None)

    def parse(self) -> Generator[str, None, None]:
        pdf_files = glob.glob(f"{self.folderpath}/candidaturas*.pdf")
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.folderpath}")

        for pdf_path in pdf_files:
            yield from self.__parse_single_file(pdf_path)

    def __parse_single_file(self, pdf_path: str) -> Generator[str, None, None]:
        doc = fitz.open(pdf_path)
        for page in doc:
            text = page.get_text()
            if not text:
                continue

            if self.fix_text is not None:
                text = self.fix_text(text)

            for line in text.split("\n"):
                yield line.strip()
