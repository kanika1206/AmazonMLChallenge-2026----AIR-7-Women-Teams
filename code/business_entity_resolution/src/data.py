from pathlib import Path

import polars as pl

from normalize import add_normalized_columns


def _read_source(path):
    return pl.read_csv(
        path, separator="\t", quote_char=None,
        schema_overrides={"entity_id": pl.String, "business_name": pl.String,
                          "business_address": pl.String, "country": pl.String},
    ).with_columns(pl.col("business_name", "business_address", "country").fill_null(""))


def load_split(dataset_dir, split):

    folder = Path(dataset_dir) / split
    s1 = _read_source(folder / f"{split}_source1.tsv")
    records = pl.concat([_read_source(folder / f"{split}_source{n}.tsv") for n in (2, 3)])
    return (add_normalized_columns(s1).with_row_index("s1_i"),
            add_normalized_columns(records).with_row_index("i"))


def load_truth(dataset_dir, s1, records):

    truth = pl.read_csv(Path(dataset_dir) / "train" / "train_ground_truth.tsv", separator="\t", quote_char=None,
                        schema_overrides={"source1_entity_id": pl.String, "matched_entity_ids": pl.String})
    return (truth.select(s1_id="source1_entity_id", rec_id=pl.col("matched_entity_ids").str.split(","))
            .explode("rec_id").filter(pl.col("rec_id").is_not_null() & (pl.col("rec_id") != ""))
            .join(s1.select("s1_i", s1_id="entity_id"), on="s1_id")
            .join(records.select("i", rec_id="entity_id"), on="rec_id")
            .select("i", "s1_i"))


def as_ids(pairs, s1, records):

    return (pairs.join(s1.select("s1_i", s1_id="entity_id"), on="s1_i")
            .join(records.select("i", record_id="entity_id"), on="i")
            .select("s1_id", "record_id"))


def write_id_lists(path, pairs, s1_ids, column):

    lists = (pairs.unique().sort("s1_id", "record_id")
             .group_by("s1_id", maintain_order=True).agg(pl.col("record_id").str.join(",")))
    (pl.DataFrame({"s1_id": s1_ids})
     .join(lists, on="s1_id", how="left", maintain_order="left")
     .select(source1_entity_id="s1_id", **{column: "record_id"})
     .write_csv(path, separator="\t", quote_style="never"))
