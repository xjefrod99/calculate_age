"""DataFrame extension for age calculation."""

import datetime
from typing import Optional, Union
import pandas as pd
import polars as pl


def _days_pd(df, date_col, reference_date):
    if isinstance(reference_date, str):
        ref_series = pd.to_datetime(df[reference_date])
    else:
        ref = reference_date or datetime.date.today()
        ref_series = pd.Timestamp(ref)
    return (ref_series - pd.to_datetime(df[date_col])).dt.days


def _days_pl(date_col, reference_date):
    if isinstance(reference_date, str):
        ref_expr = pl.col(reference_date)
    else:
        ref = reference_date or datetime.date.today()
        ref_expr = pl.lit(ref).cast(pl.Date)
    return (ref_expr - pl.col(date_col)).dt.total_days()


def _dispatch(df, date_col, reference_date, col_name, pd_transform, pl_transform):
    if isinstance(df, pd.DataFrame):
        df = df.copy()
        df[col_name] = pd_transform(_days_pd(df, date_col, reference_date))
        return df
    elif isinstance(df, pl.DataFrame):
        return df.with_columns(pl_transform(_days_pl(date_col, reference_date)).alias(col_name))
    raise ValueError("Unsupported: Pandas/Polars only.")


def calculate_age(df, date_col: str, reference_date: Union[datetime.date, str, None] = None):
    """Age in whole years (int)."""
    return _dispatch(
        df, date_col, reference_date, "age",
        pd_transform=lambda days: days.floordiv(365.25).astype(int),
        pl_transform=lambda days: (days / 365.25).floor().cast(pl.Int32),
    )


def calculate_age_indays(df, date_col: str, reference_date: Union[datetime.date, str, None] = None):
    """Age in total days (int)."""
    return _dispatch(
        df, date_col, reference_date, "age_in_days",
        pd_transform=lambda days: days.astype(int),
        pl_transform=lambda days: days.cast(pl.Int32),
    )


def calculate_age_exact(df, date_col: str, reference_date: Union[datetime.date, str, None] = None):
    """Age in years rounded to 2 decimal places (float)."""
    return _dispatch(
        df, date_col, reference_date, "age_exact",
        pd_transform=lambda days: (days / 365.25).round(2),
        pl_transform=lambda days: (days / 365.25).round(2),
    )
