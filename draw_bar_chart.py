import matplotlib.pyplot as plt
import pandas as pd

def yearly_gdp_bar(df: pd.DataFrame, year: int) -> None:
    year = str(year)
    df[year] = pd.to_numeric(df[year], errors="coerce")
    grouped = df.groupby("Continent")[year].sum()
    plt.figure(figsize=(10, 6))
    plt.bar(grouped.index, grouped.values)
    plt.xlabel("Continent")
    plt.ylabel("GDP")
    plt.title(f"GDP by Continent in {year}")
    plt.tight_layout()

def regional_gdp_bar(df: pd.DataFrame, region: str, year: int) -> None:
    year = str(year)

    # ensure numeric
    df[year] = pd.to_numeric(df[year], errors="coerce")

    # filter region
    region_df = df[df["Continent"].astype(str).str.strip().str.lower() == region.lower().strip()]

    if region_df.empty:
        print(f"❌ No data for region '{region}'")
        return

    values = region_df[year]
    if values.isna().all():
        print(f"❌ All GDP values are NaN for region '{region}' year {year}")
        return

    plt.figure(figsize=(12, 6))
    plt.bar(region_df["Country Name"], values)
    plt.xticks(rotation=90)
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.title(f"GDP by Country — {region} ({year})")
    plt.tight_layout()