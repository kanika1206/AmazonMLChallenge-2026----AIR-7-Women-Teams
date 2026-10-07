from pathlib import Path

import polars as pl

PAIR = ["s1_id", "record_id"]


def load_records(test_dir):

    s1, s2, s3 = (_read_source(Path(test_dir) / f"test_source{n}.tsv") for n in (1, 2, 3))
    return s1, pl.concat([s2, s3])


def _read_source(path):
    return pl.read_csv(
        path,
        separator="\t",
        quote_char=None,
        schema_overrides={"business_name": pl.String, "business_address": pl.String},
    ).with_columns(pl.col("business_address").fill_null(""))


def read_pairs(path):
    return (
        pl.read_csv(path, separator="\t", quote_char=None, schema_overrides={"matched_entity_ids": pl.String})
        .select(s1_id="source1_entity_id", record_id=pl.col("matched_entity_ids").str.split(","))
        .explode("record_id")
        .filter(pl.col("record_id").is_not_null() & (pl.col("record_id") != ""))
    )


def write_matches(path, pairs, s1_ids):
    assert pairs["record_id"].is_unique().all(), "a record is matched to two entities"
    matches = pairs.group_by("s1_id", maintain_order=True).agg(pl.col("record_id").str.join(","))
    (
        pl.DataFrame({"s1_id": s1_ids})
        .join(matches, on="s1_id", how="left", maintain_order="left")
        .rename({"s1_id": "source1_entity_id", "record_id": "matched_entity_ids"})
        .write_csv(path, separator="\t", quote_style="never")
    )


def unmatched(records, pairs):
    return records.join(pairs, left_on="entity_id", right_on="record_id", how="anti")


def without(pairs, removed):
    return pairs.join(removed.select(PAIR), on=PAIR, how="anti", maintain_order="left")


def with_details(pairs, s1, records):
    return pairs.join(
        s1.select(s1_id="entity_id", s1_name="business_name", s1_address="business_address"),
        on="s1_id",
    ).join(
        records.select(record_id="entity_id", record_name="business_name", record_address="business_address"),
        on="record_id",
    )
