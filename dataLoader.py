import pandas as pd
from typing import Dict, Any

class DataLoader:
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """Load CSV file"""
        try:
            return pd.read_csv(filepath)
        except Exception:
            return pd.DataFrame()
    
    def clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean numeric columns using functional programming"""
        if df.empty:
            return df
        
        # Find year columns using filter and lambda
        is_year = lambda col: str(col).strip().isdigit() and len(str(col).strip()) == 4
        year_columns = list(filter(is_year, df.columns))
        
        # Clean each year column using map
        clean_column = lambda col: pd.to_numeric(
            df[col].astype(str).str.replace(',', ''), 
            errors='coerce'
        )
        
        cleaned_data = list(map(clean_column, year_columns))
        
        # Update dataframe
        for i, col in enumerate(year_columns):
            df[col] = cleaned_data[i]
        
        return df
    
    def filter_by_config(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """Filter data based on configuration with case-insensitive matching"""
        filtered_df = df.copy()
        
        region = config.get('region', '').strip()
        country = config.get('country', '').strip()
        
        # Case-insensitive filtering using lambda
        if region:
            region_lower = region.lower()
            region_filter = lambda row: str(row['Continent']).strip().lower() == region_lower
            filtered_df = filtered_df[filtered_df.apply(region_filter, axis=1)]
        
        if country:
            country_lower = country.lower()
            country_filter = lambda row: str(row['Country Name']).strip().lower() == country_lower
            filtered_df = filtered_df[filtered_df.apply(country_filter, axis=1)]
        
        return filtered_df