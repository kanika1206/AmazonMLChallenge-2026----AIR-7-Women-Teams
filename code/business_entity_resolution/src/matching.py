import polars as pl

def macro_f05(predicted, truth, n_entities):

    tp = predicted.join(truth, on=["i", "s1_i"]).group_by("s1_i").agg(tp=pl.len())
    rows = (predicted.group_by("s1_i").agg(n_pred=pl.len())
            .join(truth.group_by("s1_i").agg(n_true=pl.len()), on="s1_i", how="full", coalesce=True)
            .join(tp, on="s1_i", how="left").fill_null(0))
    precision = pl.col("tp") / pl.col("n_pred")
    recall = pl.col("tp") / pl.col("n_true")
    f = pl.when(pl.col("tp") == 0).then(0.0).otherwise(1.25 * precision * recall / (0.25 * precision + recall))
    return (rows.select(f.sum()).item() + n_entities - rows.height) / n_entities
