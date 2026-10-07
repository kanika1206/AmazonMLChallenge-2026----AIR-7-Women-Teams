import polars as pl
from rapidfuzz import fuzz, process

from .text import name_key, normalize_address

WORKERS = 8


def name_scores(s1_names, record_names):
    s1_keys = [name_key(name) for name in s1_names]
    record_keys = [name_key(name) for name in record_names]
    return pl.Series(process.cpdist(s1_keys, record_keys, scorer=fuzz.token_sort_ratio, workers=WORKERS))


def address_scores(s1_addresses, record_addresses):
    s1_normalized = [normalize_address(address) for address in s1_addresses]
    record_normalized = [normalize_address(address) for address in record_addresses]
    return pl.Series(process.cpdist(s1_normalized, record_normalized, scorer=fuzz.token_set_ratio, workers=WORKERS))
