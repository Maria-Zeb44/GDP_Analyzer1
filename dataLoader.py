import pandas as pd
from typing import Dict, Any

class DataLoader:
    def load_csv(self, filepath: str) -> pd.DataFrame:
        """Load CSV using pandas"""
        try:
            return pd.read_csv(filepath)
        except FileNotFoundError:
            print(f"Error: File '{filepath}' not found")
            return pd.DataFrame()
        except Exception as e:
            print(f"Error loading CSV: {e}")
            return pd.DataFrame()
    
    def clean_numeric_columns(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean numeric columns using functional programming"""
        # finding cols
        is_year_column = lambda col: str(col).strip().isdigit() and len(str(col).strip()) == 4
        year_columns = list(filter(is_year_column, df.columns))
        
        # Cleanning cols
        clean_func = lambda x: pd.to_numeric(x.astype(str).str.replace(',', ''), errors='coerce')
        df[year_columns] = df[year_columns].applymap(clean_func)
        
        return df
    
    def filter_by_config(self, df: pd.DataFrame, config: Dict[str, Any]) -> pd.DataFrame:
        """Filter data based on configuration"""
        filtered_df = df.copy()
        
        # Filtering by regions
        if config.get('region'):
            filtered_df = filtered_df[filtered_df['Continent'] == config['region']]
        
        # Filtering by countries
        if config.get('country'):
            filtered_df = filtered_df[filtered_df['Country Name'] == config['country']]
        
        return filtered_df

if __name__ == "__main__":
    # Testing code
    loader = DataLoader()
    df = loader.load_csv("gdp_cleaned_fixed.csv")
    
    if not df.empty:
        print(f"Loaded {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"Columns: {list(df.columns)[:5]}...")  # Shows 1st 5 cols
    else:
        print("Failed to load data")