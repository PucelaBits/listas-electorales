from ._common import (
    clean_ocr_text,
    fill_missing_numbers,
    fix_ocr_numbers,
    register_fixer,
)


# BOA 55, err.pdf (BOA 53, página 1370): Huesca, candidatura nº 3.
# «UNION ARAGONESISTA-CHUNTA ARAGONESISTA» CHA must read «CHUNTA ARAGONESISTA» CHA.
# The scanned text is split across several lines with OCR holes ("UNJON",
# "ARAGONESIST A"); replace each whole chunk with the corrected name only
# (the name as printed in the other provinces).@register_fixer("aragon", 1991, 5)
def fix_aragon_1991_05(text: str) -> str:
    # Summary list of candidaturas (top of the Huesca page)
    text = text.replace(
        "«UNJON\nARAGONESIST A-CHUNT A-\nARAGONESIST A CHA».",
        "«CHUNTA\nARAGONESISTA» CHA.",
    )
    # Candidatura nº 3 header (same page, lower)
    text = text.replace(
        "N.lI 3.-«UNION\nARAGONESISTA-CHUNTA\nARA-\nGONESIST A» CHA",
        "N.lI 3.-«CHUNTA\nARAGONESISTA» CHA",
    )
    return text


@register_fixer("aragon", 1995, 5)
def fix_aragon_1995_05(text: str) -> str:
    print(text)
    # Errata (err.pdf)
    text = text.replace("PEDRAFITA FERRER", "PIEDRAFITA FERRER")
    # Fix OCR
    text = fix_ocr_numbers(text)
    text = text.replace("II.-", "11.-")
    text = text.replace("H.-", "11.-")
    text = text.replace("I.", "1.")
    text = clean_ocr_text(text)
    return text


@register_fixer("aragon", 1999, 6)
def fix_aragon_1999_06(text: str) -> str:
    # Erratas (err.pdf)
    text = text.replace("MARTA DOLORES CANUDO AZOR", "MARÍA DOLORES CANUDO AZOR")
    # Make it easier to parse
    text = text.replace(
        "4.—S.O.S. NATURALEZA - LOS VERDES",
        "Candidatura núm.: 4. S.O.S. NATURALEZA - LOS VERDES",
    )
    return text


@register_fixer("aragon", 2003, 5)
def fix_aragon_2003_05(text: str) -> str:
    # Facilitate parsing
    text = text.replace("Nº ", "Candidatura núm.: ")
    if "2. VICTOR PEREZ ROCHE" in text:
        start_line = "2. VICTOR PEREZ ROCHE"
        end_line = "19. MARIA RUIZ GUERRERO"
        text = fill_missing_numbers(text, start_line, end_line, start_number=1)
    return text


def number_candidates(text: str, last_number: int | None = None) -> str:
    lines = text.split("\n")
    result = []
    counter = last_number

    for line in lines:
        stripped_line = line.lstrip()  # Remove leading whitespace for accurate checking

        # Check if the line is a candidate name
        if stripped_line.startswith(("DON ", "DOÑA ")) and counter is not None:
            # Add the number and increment the counter
            result.append(f"{counter}. {line}")
            counter += 1
            print(f"Numbering candidate: {line} as {counter - 1}")
        else:
            # Reset the counter if we hit a new list header or the "SUPLENTES" section
            upper_line = stripped_line.upper()
            if "CANDIDATURA NÚM." in upper_line or "SUPLENTES" in upper_line:
                counter = 1
                print(f"Resetting counter to 1 due to line: {line}")

            # Append the non-candidate line exactly as it was
            result.append(line)

    return "\n".join(result), counter


_ARAGON_2007_05_LAST_NUMBER = None


@register_fixer("aragon", 2007, 5)
def fix_aragon_2007_05(text: str) -> str:
    # Errata (err.pdf)
    text = text.replace(
        "DOÑA MONSERRAT VILLAGRASA ALCANTARA",
        "DOÑA MONTSERRAT VILLAGRASA ALCANTARA",
    )
    text = text.replace("NIEVES IBERS VUELTA", "NIEVES IBEAS VUELTA")
    # Facilitate parsing
    text = text.replace("Nº ", "Candidatura núm.: ")
    text = text.replace("Nº", "Candidatura núm.: ")
    # Fill missing numbers
    global _ARAGON_2007_05_LAST_NUMBER
    print(_ARAGON_2007_05_LAST_NUMBER)
    text, last_number = number_candidates(text, last_number=_ARAGON_2007_05_LAST_NUMBER)
    _ARAGON_2007_05_LAST_NUMBER = last_number
    print(last_number)
    print(repr(text))
    return text


@register_fixer("aragon", 2011, 5)
def fix_aragon_2011_05(text: str) -> str:
    # Facilitate parsing
    text = text.replace("Nº ", "Candidatura núm.: ")
    return text
