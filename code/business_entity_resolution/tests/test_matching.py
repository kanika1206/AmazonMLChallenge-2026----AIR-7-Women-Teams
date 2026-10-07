import polars as pl
import pytest

from matching import macro_f05


def test_macro_f05_includes_correct_singletons():
    truth = pl.DataFrame({"i": [0, 1], "s1_i": [0, 0]})
    predicted = pl.DataFrame({"i": [0, 1, 2], "s1_i": [0, 0, 0]})
    assert macro_f05(predicted, truth, 2) == pytest.approx((5 / 7 + 1) / 2)


def test_macro_f05_penalizes_false_singleton_matches():
    truth = pl.DataFrame({"i": [0], "s1_i": [0]})
    predicted = pl.DataFrame({"i": [0, 1], "s1_i": [0, 1]})
    assert macro_f05(predicted, truth, 2) == 0.5


def test_macro_f05_perfect_matches():
    truth = pl.DataFrame({"i": [0, 1], "s1_i": [0, 0]})
    assert macro_f05(truth, truth, 2) == 1.0
