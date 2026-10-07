import polars as pl

from postprocess.records import write_matches

def pairs(*rows):
    return pl.DataFrame(rows, schema=["s1_id", "record_id"], orient="row")


def test_write_matches_keeps_id_order_and_writes_empty_rows(tmp_path):
    path = tmp_path / "matching_results.tsv"
    write_matches(path, pairs(("S1-b", "S3-2"), ("S1-b", "S2-7")), pl.Series(["S1-a", "S1-b"]))
    assert path.read_text() == "source1_entity_id\tmatched_entity_ids\nS1-a\t\nS1-b\tS3-2,S2-7\n"
