from typing import List, Dict, Any
import pandas as pd

class DataProcessor:
    def extract_year_data(self, df: pd.DataFrame, year: int) -> List[float]:
        """Extract GDP values for specific year using functional approach"""
        year_str = str(year)
        if year_str in df.columns:
            # Get values, remove NaN
            values = df[year_str].dropna().tolist()
            # Filter out any remaining NaN using functional programming
            return list(filter(lambda x: not pd.isna(x), values))
        return []
    

    
    def calculate_statistics(self, gdp_values: List[float], operation: str) -> float:
        """Calculate statistics using functional programming"""
        if not gdp_values:
            return 0.0
        
        if operation == "average":
            return sum(gdp_values) / len(gdp_values)
        elif operation == "sum":
            return sum(gdp_values)
        else:
            return 0.0
    
    def process_data(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function - uses functional programming"""
        # Filtering by region
        if config.get("region"):
            df = df[df["Continent"] == config["region"]]
            print(f"DEBUG: After region filter '{config['region']}': {len(df)} rows")
        
        # Filtering by country
        if config.get("country"):
            df = df[df["Country Name"] == config["country"]]
            print(f"DEBUG: After country filter '{config['country']}': {len(df)} rows")
        
        # Check if we have data
        if df.empty:
            print(f"DEBUG: No data after filtering")
            gdp_values = []
        else:
            # Extracting data for specific year
            year = config["year"]
            print(f"DEBUG: Extracting data for year {year}")
            gdp_values = self.extract_year_data(df, year)
            print(f"DEBUG: Found {len(gdp_values)} GDP values for {year}")
            if gdp_values:
                print(f"DEBUG: Sample values: {gdp_values[:3]}")
        
        # Calculate results
        result = self.calculate_statistics(gdp_values, config.get("operation", "average"))
        
        return {
            "operation": config.get("operation", "average"),
            "year": config["year"],
            "region": config.get("region", "All"),
            "country": config.get("country", "All"),
            "result": result,
            "data_points": len(gdp_values)
        }
