import polars as pl
from rapidfuzz import fuzz, process
from rapidfuzz.distance import JaroWinkler

WORKERS = 8


def _score(left, right, scorer):
    return pl.Series(process.cpdist(left, right, scorer=scorer, workers=WORKERS))


def _with_text(pairs, s1, records):
    columns = ["core", "addr"]
    return (pairs.join(records.select("i", *columns), on="i")
            .join(s1.select("s1_i", *columns), on="s1_i", suffix="_1"))


def match_features(top, s1, records):
    c = _with_text(top, s1, records)
    return c.with_columns(
        ratio=_score(c["core"], c["core_1"], fuzz.ratio),
        sort_ratio=_score(c["core"], c["core_1"], fuzz.token_sort_ratio),
        partial=_score(c["core"], c["core_1"], fuzz.partial_ratio),
        jw=_score(c["core"], c["core_1"], JaroWinkler.normalized_similarity),
        addr_sort=_score(c["addr"], c["addr_1"], fuzz.token_sort_ratio),
        addr_partial=_score(c["addr"], c["addr_1"], fuzz.partial_ratio),
    ).select("i", "s1_i", "ratio", "sort_ratio", "partial", "jw", "addr_sort", "addr_partial")
