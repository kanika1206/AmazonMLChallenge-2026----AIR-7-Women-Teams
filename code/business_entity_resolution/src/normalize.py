import re
from concurrent.futures import ProcessPoolExecutor

import polars as pl
from unidecode import unidecode

WORKERS = 8


STOPWORDS = {"the", "and", "of", "et", "de", "du", "des", "la", "le", "les"}


ADDRESS_WORDS = {
    "street": "st", "str": "st", "saint": "st", "road": "rd", "avenue": "ave", "av": "ave", "drive": "dr",
    "lane": "ln", "boulevard": "blvd", "bd": "blvd", "court": "ct", "place": "pl", "highway": "hwy",
    "parkway": "pkwy", "circle": "cir", "apartment": "apt", "floor": "fl", "building": "bldg",
    "near": "nr", "opposite": "opp", "r": "rue", "route": "rte", "chemin": "che", "impasse": "imp",
    "square": "sq", "suite": "ste",
}


ADDRESS_NOISE = {"null", "na", "no", "n", "nan", "none"}


WORD = re.compile(r"[a-z0-9]+")


DIGITS = re.compile(r"\d+")


def _ascii_lower(text):
    return (text if text.isascii() else unidecode(text)).lower()


def normalize_address(address):

    text = _ascii_lower(address)
    tokens = [ADDRESS_WORDS.get(t, t) for t in WORD.findall(text) if t not in ADDRESS_NOISE]
    numbers = sorted({n.lstrip("0") or "0" for n in DIGITS.findall(text)})
    return " ".join(tokens), " ".join(numbers)


def _names(chunk):
    return [normalize_name(name) for name in chunk]


def _addresses(chunk):
    return [normalize_address(address) for address in chunk]


def _in_parallel(fn, values, chunk_size=50_000):
    chunks = [values[i:i + chunk_size] for i in range(0, len(values), chunk_size)]
    with ProcessPoolExecutor(WORKERS) as pool:
        return [item for part in pool.map(fn, chunks) for item in part]


def add_normalized_columns(records):
    names = _in_parallel(_names, records["business_name"].to_list())
    addresses = _in_parallel(_addresses, records["business_address"].to_list())
    core = [c for c, _ in names]
    return records.with_columns(
        core=pl.Series(core, dtype=pl.String),
        addr=pl.Series([a for a, _ in addresses], dtype=pl.String),
        nums=pl.Series([n for _, n in addresses], dtype=pl.String),
    )


def normalize_name(name):
    text = _ascii_lower(name)
    text = text.replace("&", " and ").replace("+", " and ")
    tokens = WORD.findall(text)
    core = [t for t in tokens if t not in STOPWORDS] or tokens
    core = [t for i, t in enumerate(core) if i == 0 or t != core[i - 1]]
    return " ".join(core), ""
