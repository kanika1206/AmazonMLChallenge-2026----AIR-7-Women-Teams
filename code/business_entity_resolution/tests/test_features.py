import polars as pl

from features import match_features
from normalize import normalize_address, normalize_name
from postprocess.pair_features import address_scores, name_scores


def test_basic_normalization_retains_legal_words():
    assert normalize_name("ACME & Sons LLC") == ("acme sons llc", "")
    assert normalize_address("012 Main Street") == ("012 main st", "12")


def test_generic_similarity_columns_on_identical_text():
    s1 = pl.DataFrame({"s1_i": [0], "core": ["acme sons llc"], "addr": ["12 main st"]})
    records = pl.DataFrame({"i": [0], "core": ["acme sons llc"], "addr": ["12 main st"]})
    result = match_features(pl.DataFrame({"i": [0], "s1_i": [0]}), s1, records)
    assert result.row(0) == (0, 0, 100.0, 100.0, 100.0, 1.0, 100.0, 100.0)


def test_generic_pair_scoring():
    assert name_scores(["ACME & Sons"], ["Acme and Sons"]).to_list() == [100.0]
    assert address_scores(["12 Main St"], ["12 Main Street"]).to_list() == [100.0]
