import pandas as pd
from dataLoader import DataLoader


def test_clean_numeric_columns_converts_commas():
    df = pd.DataFrame({"1960": ["1,000", "2,500", None], "Country Name": ["A", "B", "C"]})
    cleaned = DataLoader().clean_numeric_columns(df.copy())
    assert pd.api.types.is_numeric_dtype(cleaned["1960"])
    # None should be preserved as NaN (pytest will compare to None via list conversion)
    assert cleaned["1960"].tolist() == [1000, 2500, None]
