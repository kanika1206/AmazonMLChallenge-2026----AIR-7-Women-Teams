import lightgbm as lgb
import polars as pl

THREADS = 8


def _matrix(frame, columns):
    return frame.select(pl.col(columns).cast(pl.Float32)).to_numpy()


def train(frame, columns, labels, params, rounds):
    return lgb.train(params, lgb.Dataset(_matrix(frame, columns), labels, feature_name=columns), rounds)


def predict(model, frame, columns):
    return pl.Series(model.predict(_matrix(frame, columns), num_threads=THREADS)).cast(pl.Float32)
