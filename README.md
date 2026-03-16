# calculate-age

[![PyPI version](https://badge.fury.io/py/calculate-age.svg)](https://pypi.org/project/calculate-age/)
[![Downloads](https://img.shields.io/pypi/dm/calculate-age)](https://pypistats.org/packages/calculate-age)

(https://pypistats.com/packages/calculate-age)

Calculate ages from date columns in Pandas/Polars DataFrames.

## Install
```bash
pip install calculate-age
```

## Usage


### Accessor API (chainable)
```python
import pandas as pd
import polars as pl
import calculate_age  # registers accessors on import

#init a df
df = pd.DataFrame({
    "name":       ["Alice", "Bob"],
    "birth_date": pd.to_datetime(["1990-01-01", "2000-06-15"])
})

# Pandas
df = df.calculate_age("birth_date")
# Adds column "age" (whole years vs today)
#    name  birth_date  age
# 0  Alice  1990-01-01   36
# 1  Bob    2000-06-15   25

df = df.calculate_age_indays("birth_date")
# Adds column "age_in_days" (total days vs today)
#    name  birth_date  age_in_days
# 0  Alice  1990-01-01        13223
# 1  Bob    2000-06-15         9374

df = df.calculate_age_exact("birth_date")
# Adds column "age_exact" (years to 2 decimal places vs today)
#    name  birth_date  age_exact
# 0  Alice  1990-01-01      36.20
# 1  Bob    2000-06-15      25.75


# Polars
df_pl = df_pl.calculate_age("birth_date")
df_pl = df_pl.calculate_age_indays("birth_date")
df_pl = df_pl.calculate_age_exact("birth_date")
```

### Function API
```python
import datetime
from calculate_age import calculate_age, calculate_age_indays, calculate_age_exact
import pandas as pd
import polars as pl

# Pandas
df = pd.DataFrame({"birth_date": pd.to_datetime(["1990-01-01"])})
result = calculate_age(df, "birth_date")                              # vs today
result = calculate_age(df, "birth_date", datetipip install buildme.date(2026, 3, 15))  # vs a fixed date
result = calculate_age(df, "birth_date", "hire_date")                 # vs another column
result = calculate_age_indays(df, "birth_date")                       # age in total days
result = calculate_age_exact(df, "birth_date")                        # age in years (2 decimals)

# Polars
df_pl = pl.DataFrame({"birth_date": ["1990-01-01"]}).with_columns(
    pl.col("birth_date").str.strptime(pl.Date, "%Y-%m-%d")
)
result = calculate_age(df_pl, "birth_date")
```
