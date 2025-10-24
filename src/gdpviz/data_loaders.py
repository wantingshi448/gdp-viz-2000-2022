from pandas_datareader import wb
import pandas as pd
DISPLAY_ALIASES = {
    "United States": "USA",
    "United Kingdom": "UK",
    "Brazil": "Brazil",
    "Japan": "Japan",
    "China": "China",
    "Germany": "Germany",
    "Switzerland": "Switzerland",
}
WB_ISO2 = ["US", "GB", "BR", "JP", "CN", "DE", "CH"]
def fetch_worldbank_gdp(series_code: str = "NY.GDP.MKTP.KD",
                        start: int = 2000,
                        end: int = 2022) -> pd.DataFrame:
    """
    Fetch GDP data from World Bank via pandas-datareader.
    Returns tidy DataFrame with columns: country, year, value.
    """
    df = wb.download(indicator=series_code, country=WB_ISO2, start=start, end=end)
    df = df.reset_index().rename(columns={series_code: "value"})
    df["country"] = df["country"].replace(DISPLAY_ALIASES)
    df = df[pd.to_numeric(df["year"], errors="coerce").notna()].copy()
    df["year"] = df["year"].astype(int)
    df = df[["country", "year", "value"]].sort_values(["country", "year"]).reset_index(drop=True)
    return df
