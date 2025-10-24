import pandas as pd
def drop_missing_and_nonpositive(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows where GDP is NaN or <= 0.
    """
    out = df.dropna(subset=["value"]).copy()
    out = out[out["value"] > 0]
    return out
def to_wide(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert tidy (country, year, value) to wide format with years as index
    and countries as columns.
    """
    wide = df.pivot(index="year", columns="country", values="value").sort_index()
    wide.columns.name = None
    return wide
