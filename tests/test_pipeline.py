from gdpviz.data_loaders import fetch_worldbank_gdp
from gdpviz.cleaning import drop_missing_and_nonpositive, to_wide
def test_fetch_basic_small_range():
    df = fetch_worldbank_gdp(start=2000, end=2002)
    assert {"country", "year", "value"} <= set(df.columns)
    assert df["year"].between(2000, 2002).all()
    assert df["country"].nunique() >= 5
def test_clean_and_wide():
    df = fetch_worldbank_gdp(start=2000, end=2001)
    clean = drop_missing_and_nonpositive(df)
    assert (clean["value"] > 0).all()
    wide = to_wide(clean)
    assert wide.index.min() >= 2000
    assert wide.shape[1] == clean["country"].nunique()
