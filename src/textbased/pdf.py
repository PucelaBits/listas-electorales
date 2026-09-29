import glob
from collections.abc import Generator

import pymupdf

from common import logger

from .parse_fixes import PARSE_FIXES
from .pdf_parsing.helpers import find_min_max_x, is_double_column, parse_n_column_page

HARCODED_COLUMN_FIX = {
    ("canarias", 2015, 5): 1,
    ("cantabria", 2011, 5): 1,
    ("cataluna", 1988, 5): 3,
    ("cataluna", 1992, 3): 3,
    ("cataluna", 1995, 11): 3,
    ("cataluna", 1999, 10): 3,
    ("cataluna", 2003, 11): 3,
    ("cataluna", 2006, 11): 3,
    ("castilla_la_mancha", 1999, 6): 1,
    ("castilla_la_mancha", 2007, 5): 3,
    ("murcia", 2003, 5): 2,
    ("pais_vasco", 1998, 10): [1 / 3, 2 / 3],
    ("pais_vasco", 1994, 10): 3,
    ("pais_vasco", 1990, 10): 3,
}


class PDFReader:
    def __init__(self, folderpath: str, region: str, year: int, month: int):
        self.folderpath = folderpath
        self.fix_text = PARSE_FIXES.get((region, year, month), None)
        self.column_count = HARCODED_COLUMN_FIX.get((region, year, month), None)

    def parse(self) -> Generator[str, None, None]:
        pdf_files = glob.glob(f"{self.folderpath}/candidaturas*.pdf")
        if not pdf_files:
            raise FileNotFoundError(f"No PDF files found in {self.folderpath}")

        pdf_files.sort()  # Ensure consistent order
        for pdf_path in pdf_files:
            yield from self.__parse_single_file(pdf_path)

    def __parse_single_file(self, pdf_path: str) -> Generator[str, None, None]:
        doc = pymupdf.open(pdf_path)
        if self.column_count is None:
            if is_double_column(doc):
                logger.debug(
                    f"Detected double-column layout in {pdf_path}. Using double-column parsing."
                )
                self.column_count = 2
            else:
                logger.debug(
                    f"Detected single-column layout in {pdf_path}. Using single-column parsing."
                )
                self.column_count = 1
        elif isinstance(self.column_count, list):
            logger.debug(
                f"Using hardcoded {len(self.column_count) + 1}-column layout for {pdf_path}."
            )
        else:
            logger.debug(
                f"Using hardcoded {self.column_count}-column layout for {pdf_path}."
            )

        for page in doc:
            column_count = self.column_count
            column_splits = None
            if isinstance(self.column_count, list):
                min_x, max_x = find_min_max_x(page.get_text("words", flags=0))
                if max_x - min_x <= 0:
                    raise ValueError(
                        "Invalid word bounding boxes: zero or negative width"
                    )
                column_splits = [min_x + (max_x - min_x) * split for split in self.column_count]
                column_count = len(self.column_count) + 1
            text = parse_n_column_page(page, column_count, column_splits=column_splits)

            if not text:
                continue

            if self.fix_text is not None:
                text = self.fix_text(text)

            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                yield line
