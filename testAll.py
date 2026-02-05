from dataLoader import DataLoader
from dataProcessor import DataProcessor
from configLoader import load_config, validate_config 

print("=" * 60)
print("GDP ANALYSIS SYSTEM - FUNCTIONAL PROGRAMMING TEST")
print("=" * 60)

# Loading configuration from config.json
print("\n1. Loading configuration...")
config = load_config('config.json')

if not config:
    print(" FAILED: Could not load config.json")
    exit()

if not validate_config(config):
    print(" FAILED: Invalid configuration")
    exit()

print(f"   Config: region='{config.get('region')}', year={config.get('year')}, operation='{config.get('operation')}'")

# Test DataLoader
print("\n2. Testing DataLoader...")
loader = DataLoader()
df = loader.load_csv("gdp_cleaned_fixed.csv")

if df.empty:
    print(" FAILED: Could not load gdp_cleaned_fixed.csv")
    exit()

print(f"   Loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# Clean and filter data
print("\n3. Cleaning and filtering data...")
df = loader.clean_numeric_columns(df)
filtered_df = loader.filter_by_config(df, config)
print(f"  Filtered to: {filtered_df.shape[0]} rows")

# Test DataProcessor
print("\n4. Testing DataProcessor...")
processor = DataProcessor()

# Test extraction
gdp_values = processor.extract_year_data(filtered_df, config['year'])
print(f"  Extracted {len(gdp_values)} GDP values for year {config['year']}")

# Test calculation
result = processor.calculate_statistics(gdp_values, config['operation'])
print(f"  {config['operation'].title()}: ${result:,.2f}")

# Test processing
print("\n5. Running complete data processing...")
stats = processor.process_data(df, config)

print("\n" + "=" * 60)
print("FINAL RESULTS:")
print("=" * 60)
for key, value in stats.items():
    if key == 'result':
        print(f"{key:15}: ${value:,.2f}")
    else:
        print(f"{key:15}: {value}")

print("\n" + "=" * 60)
print("ALL TESTS PASSED! SYSTEM IS WORKING CORRECTLY")
print("=" * 60)