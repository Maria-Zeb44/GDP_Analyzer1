import matplotlib.pyplot as plt
import pandas as pd
from typing import Tuple, List

def yearly_gdp_pie(df: pd.DataFrame,year: int)->None:
    year=str(year)

    gdp_by_region=df.groupby("Continent")[year].sum()

    lable=gdp_by_region.index.tolist()
    values=gdp_by_region.values.tolist()

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=lable, autopct='%1.2f%%')
    plt.title(f"GDP Distribution by Continent ({year})")
    plt.show()

def regional_gdp_pie(df: pd.DataFrame, region: str, year: int) -> None:
    year = str(year)

    region_df=df[df["Continent"]==region]

    labels=region_df["Country Name"].tolist()
    values=region_df[year].tolist()

    plt.figure(figsize=(7, 7))
    plt.pie(values, labels=labels, autopct='%1.1f%%')
    plt.title(f"GDP Distribution in {region} ({year})")
    plt.show()