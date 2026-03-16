import datetime
import pytest
import pandas as pd
import polars as pl
from calculate_age import calculate_age, calculate_age_indays, calculate_age_exact


@pytest.fixture
def sample_pd():
    return pd.DataFrame({"dob": pd.to_datetime(["2000-01-01", "1990-06-15"])})


@pytest.fixture
def sample_pl():
    return pl.DataFrame({"dob": ["2000-01-01", "1990-06-15"]}).with_columns(
        pl.col("dob").str.strptime(pl.Date, "%Y-%m-%d")
    )


def test_pandas(sample_pd):
    ref = datetime.date(2026, 3, 15)
    result = calculate_age(sample_pd, "dob", ref)
    pd.testing.assert_series_equal(result["age"], pd.Series([26, 35], dtype=int, name="age"))


def test_polars(sample_pl):
    ref = datetime.date(2026, 3, 15)
    result = calculate_age(sample_pl, "dob", ref)
    assert result["age"].to_list() == [26, 35]


def test_default_date(sample_pd):
    result = calculate_age(sample_pd, "dob")
    assert "age" in result.columns

# ... existing fixtures ...

def test_pandas_accessor(sample_pd):
    ref = datetime.date(2026, 3, 15)
    result = sample_pd.calculate_age("dob", ref)
    pd.testing.assert_series_equal(result["age"], pd.Series([26, 35], dtype=int, name="age"))

def test_pandas_default(sample_pd):
    result = sample_pd.calculate_age("dob")
    assert "age" in result.columns

def test_polars_accessor(sample_pl):
    ref = datetime.date(2026, 3, 15)
    result = sample_pl.calculate_age("dob", ref)
    assert result["age"].to_list() == [26, 35]


# --- calculate_age_indays tests ---

def test_indays_pandas(sample_pd):
    ref = datetime.date(2026, 3, 15)
    result = calculate_age_indays(sample_pd, "dob", ref)
    # 2000-01-01 -> 2026-03-15 = 9570 days, 1990-06-15 -> 2026-03-15 = 13057 days
    assert result["age_in_days"].tolist() == [9570, 13057]


def test_indays_polars(sample_pl):
    ref = datetime.date(2026, 3, 15)
    result = calculate_age_indays(sample_pl, "dob", ref)
    assert result["age_in_days"].to_list() == [9570, 13057]


def test_indays_pandas_accessor(sample_pd):
    ref = datetime.date(2026, 3, 15)
    result = sample_pd.calculate_age_indays("dob", ref)
    assert result["age_in_days"].tolist() == [9570, 13057]


def test_indays_polars_accessor(sample_pl):
    ref = datetime.date(2026, 3, 15)
    result = sample_pl.calculate_age_indays("dob", ref)
    assert result["age_in_days"].to_list() == [9570, 13057]


# --- calculate_age_exact tests ---

def test_exact_pandas(sample_pd):
    ref = datetime.date(2026, 3, 15)
    result = calculate_age_exact(sample_pd, "dob", ref)
    assert result["age_exact"].tolist() == [26.2, 35.75]


def test_exact_polars(sample_pl):
    ref = datetime.date(2026, 3, 15)
    result = calculate_age_exact(sample_pl, "dob", ref)
    assert result["age_exact"].to_list() == [26.2, 35.75]


def test_exact_pandas_accessor(sample_pd):
    ref = datetime.date(2026, 3, 15)
    result = sample_pd.calculate_age_exact("dob", ref)
    assert result["age_exact"].tolist() == [26.2, 35.75]


def test_exact_polars_accessor(sample_pl):
    ref = datetime.date(2026, 3, 15)
    result = sample_pl.calculate_age_exact("dob", ref)
    assert result["age_exact"].to_list() == [26.2, 35.75]


# --- column-based reference date tests ---

@pytest.fixture
def sample_pd_with_ref():
    return pd.DataFrame({
        "dob": pd.to_datetime(["2000-01-01", "1990-06-15"]),
        "event_date": pd.to_datetime(["2026-03-15", "2026-03-15"]),
    })


@pytest.fixture
def sample_pl_with_ref():
    return pl.DataFrame({
        "dob": ["2000-01-01", "1990-06-15"],
        "event_date": ["2026-03-15", "2026-03-15"],
    }).with_columns(
        pl.col("dob").str.strptime(pl.Date, "%Y-%m-%d"),
        pl.col("event_date").str.strptime(pl.Date, "%Y-%m-%d"),
    )


def test_pandas_col_ref(sample_pd_with_ref):
    result = calculate_age(sample_pd_with_ref, "dob", "event_date")
    assert result["age"].tolist() == [26, 35]


def test_polars_col_ref(sample_pl_with_ref):
    result = calculate_age(sample_pl_with_ref, "dob", "event_date")
    assert result["age"].to_list() == [26, 35]


def test_indays_pandas_col_ref(sample_pd_with_ref):
    result = calculate_age_indays(sample_pd_with_ref, "dob", "event_date")
    assert result["age_in_days"].tolist() == [9570, 13057]


def test_indays_polars_col_ref(sample_pl_with_ref):
    result = calculate_age_indays(sample_pl_with_ref, "dob", "event_date")
    assert result["age_in_days"].to_list() == [9570, 13057]


def test_exact_pandas_col_ref(sample_pd_with_ref):
    result = calculate_age_exact(sample_pd_with_ref, "dob", "event_date")
    assert result["age_exact"].tolist() == [26.2, 35.75]


def test_exact_polars_col_ref(sample_pl_with_ref):
    result = calculate_age_exact(sample_pl_with_ref, "dob", "event_date")
    assert result["age_exact"].to_list() == [26.2, 35.75]
