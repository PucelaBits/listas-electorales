import re
from functools import lru_cache

# Pre-allocate particles mapping
_PARTICLES_MAP = {
    "De Los": "de los",
    "De Las": "de las",
    "De La": "de la",
    "Del": "del",
    "Al": "al",
    "De": "de",
    "Y": "y",
    "I": "i",
    "E": "e",
    "El": "el",
    "La": "la",
    "Los": "los",
    "Las": "las",
    "Da": "da",
    "Dos": "dos",
    "Di": "di",
    "Von": "von",
    "Van": "van",
}

# Pre-compile the particle regex
_PARTICLES_RE = re.compile(
    r"\b(?:{})\b".format("|".join(sorted(_PARTICLES_MAP.keys(), key=len, reverse=True)))
)

# Abbreviation for María and Francisco
# Group 1: Matches abbreviations glued to a letter using a Lookahead (?=[A-Za-zÀ-ÿ])
# Group 2: Matches standalone abbreviations (surrounded by spaces/boundaries)
# Group 3: Specifically matches standalone "Ma" so it doesn't break names like "Macarena"
_ABBR_RE = re.compile(
    r"\b(Mª|M\.[aªA]\.?|M[aªA]\.|Fco\.?|F\.co\.?)(?=[A-Za-zÀ-ÿ])|"
    r"\b(Mª|M\.[aªA]\.?|M[aªA]\.|Fco\.?|F\.co\.?)\b|"
    r"\b(Ma)\b",
    re.IGNORECASE,
)

# Pre-compile suffix regex
_SUFFIX_NAMES_RE = re.compile(r"\s*\(.+\)\s*$")


def _abbr_replacer(m: re.Match) -> str:
    """Expands the abbreviation and adds a space if it was glued."""
    if m.group(1):
        # It is glued to a letter. Add a space
        abbr = m.group(1).lower()
        return "María " if abbr.startswith("m") else "Francisco "
    elif m.group(2):
        # It is standalone. No trailing space needed.
        abbr = m.group(2).lower()
        return "María" if abbr.startswith("m") else "Francisco"
    elif m.group(3):
        # It is a standalone 'Ma'
        return "María"


def prettify_name(name: str | None) -> str | None:
    if not name:
        return None

    name = name.strip()
    if not name:
        return None

    # Expand abbreviations
    name = _ABBR_RE.sub(_abbr_replacer, name)

    name = name.title()

    # Particle downcasing (e.g. "De Los" -> "de los")
    name = _PARTICLES_RE.sub(lambda m: _PARTICLES_MAP[m.group(0)], name)

    # Remove suffixes and trailing whitespaces
    name = _SUFFIX_NAMES_RE.sub("", name)

    return name if name else None


# We use re.IGNORECASE so we don't need to manually list 'el|els|la|les'
_SUFFIX_MUNICIPALITIES_RE = re.compile(
    r"^(.+),\s*(A|As|El|Els|Es|L'|La|Las|Les|Los|O|Os|Sa|Ses)$", re.IGNORECASE
)


@lru_cache(maxsize=16384)
def prettify_municipality(name: str) -> str:
    """
    Beautifies municipality names, handling double spaces and suffixes.
    Adapted from "infoelectoral" project by Jaime Gómez-Obregón (AGPL-3.0 license).

    @copyright     Copyright (c) Jaime Gómez-Obregón
    @link          https://github.com/JaimeObregon/infoelectoral
    @license       https://www.gnu.org/licenses/agpl-3.0.en.html
    """
    # Remove double spaces
    name = " ".join(name.split())

    parts = name.split("/")
    formatted_parts = []

    for part in parts:
        # Strip each part to fix a bug in the original code where spaces
        # around slashes (e.g., " / Gasteiz") prevented capitalization.
        part = part.strip()
        if not part:
            continue

        m = _SUFFIX_MUNICIPALITIES_RE.match(part)
        if m:
            base, article = m.group(1), m.group(2)

            # 2. Handle L' natively without needing a second regex pass
            if article.upper() == "L'":
                part = f"L'{base}"
            else:
                part = f"{article.capitalize()} {base}"

        # Capitalize ONLY the first letter while preserving the rest of the string
        part = part[0].upper() + part[1:]

        formatted_parts.append(part)

    return "/".join(formatted_parts)
