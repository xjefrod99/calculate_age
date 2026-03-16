import pandas as pd
import polars as pl

from .core import calculate_age, calculate_age_indays, calculate_age_exact


@pd.api.extensions.register_dataframe_accessor("calculate_age")
class CalculateAgeAccessor:
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj

    def __call__(self, date_col, reference_date=None):
        return calculate_age(self._obj, date_col, reference_date)


@pd.api.extensions.register_dataframe_accessor("calculate_age_indays")
class CalculateAgeInDaysAccessor:
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj

    def __call__(self, date_col, reference_date=None):
        return calculate_age_indays(self._obj, date_col, reference_date)


@pd.api.extensions.register_dataframe_accessor("calculate_age_exact")
class CalculateAgeExactAccessor:
    def __init__(self, pandas_obj: pd.DataFrame):
        self._obj = pandas_obj

    def __call__(self, date_col, reference_date=None):
        return calculate_age_exact(self._obj, date_col, reference_date)


def _register_polars():
    for name, fn in [
        ("calculate_age", calculate_age),
        ("calculate_age_indays", calculate_age_indays),
        ("calculate_age_exact", calculate_age_exact),
    ]:
        if not hasattr(pl.DataFrame, name):
            def _make(f):
                def method(self, date_col, reference_date=None):
                    return f(self, date_col, reference_date)
                return method
            setattr(pl.DataFrame, name, _make(fn))


_register_polars()

__version__ = "0.1.0"
__all__ = ["calculate_age", "calculate_age_indays", "calculate_age_exact"]
