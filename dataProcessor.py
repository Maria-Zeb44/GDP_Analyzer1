from typing import List, Dict, Any
import pandas as pd
from functools import reduce

class DataProcessor:
    def extract_year_data(self, df: pd.DataFrame, year: int) -> List[float]:
        """Extract GDP values for specific year using functional approach"""
        year_str = str(year)
        
        if year_str not in df.columns or df.empty:
            return []
        
        # Filter out NaN values using lambda and filter
        values = df[year_str].tolist()
        non_nan_values = list(filter(lambda x: not pd.isna(x), values))
        
        return list(map(float, non_nan_values))
    
    def calculate_statistics(self, gdp_values: List[float], operation: str) -> float:
        """Calculate statistics using functional programming"""
        if not gdp_values:
            return 0.0
        
        # Define operations as lambda functions
        operations = {
            'average': lambda vals: reduce(lambda x, y: x + y, vals) / len(vals),
            'sum': lambda vals: reduce(lambda x, y: x + y, vals),
            'min': lambda vals: reduce(lambda x, y: x if x < y else y, vals),
            'max': lambda vals: reduce(lambda x, y: x if x > y else y, vals)
        }
        
        if operation in operations:
            return operations[operation](gdp_values)
        else:
            return 0.0
    
    def process_data(self, df: pd.DataFrame, config: Dict[str, Any]) -> Dict[str, Any]:
        """Main processing function - uses functional programming"""
        year = config.get("year")
        operation = config.get("operation", "average")
        
        # Extract GDP values
        gdp_values = self.extract_year_data(df, year)
        
        # Calculate result
        result = self.calculate_statistics(gdp_values, operation)
        
        # Get region and country from filtered data
        region = config.get("region", "All")
        country = config.get("country", "All")
        
        # If we have data, get actual region/country
        if not df.empty:
            if region == "All" and 'Continent' in df.columns:
                region = df['Continent'].iloc[0] if len(df) == 1 else "Multiple"
            if country == "All" and 'Country Name' in df.columns:
                country = df['Country Name'].iloc[0] if len(df) == 1 else "Multiple"
        
        return {
            "operation": operation,
            "year": year,
            "region": region,
            "country": country,
            "result": result,
            "data_points": len(gdp_values)
        }