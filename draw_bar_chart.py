import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def yearly_gdp_bar(df: pd.DataFrame, year: int) -> None:
    """
    Draw a bar chart of GDP by Continent for a given year
    """
    year = str(year)
    
    # Sum GDP by continent
    gdp_by_region = df.groupby("Continent")[year].sum()
    
    # Labels and values
    labels = gdp_by_region.index.tolist()
    values = gdp_by_region.values.tolist()
    

    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='skyblue')
    plt.xlabel("Continent")
    plt.ylabel("GDP ")
    plt.title(f"GDP by Continent in {year}")
    plt.show()


    

def regional_gdp_bar(df: pd.DataFrame, region: str, year: int) -> None:
    """
    Draw a bar chart of GDP for each country in a given region and year
    """
    year = str(year)
    
    # Filter countries by region
    region_df = df[df["Continent"] == region]
    
    # Labels and values
    labels = region_df["Country Name"].tolist()
    values = region_df[year].tolist()


    plt.figure(figsize=(10, 6))
    plt.bar(labels, values, color='salmon')
    plt.xlabel("Country")
    plt.ylabel(f"GDP in {year}")
    plt.title(f"GDP by Country in {year}")
   
    plt.show()