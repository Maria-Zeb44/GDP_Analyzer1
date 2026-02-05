import pandas as pd

print("=== GDP CSV Cleaner ===")

# 1. Read CSV
print("1. Loading CSV...")
df = pd.read_csv('gdp_with_continent_filled.csv')
print(f"   Original: {df.shape[0]} rows, {df.shape[1]} columns")

# 2. Show current numeric columns with comma issues
print("\n2. Checking numeric columns with comma issues...")

# Get year columns (1960, 1961, etc.)
year_columns = []
for col in df.columns:
    try:
        # Check if column name is a 4-digit year
        if str(col).strip().isdigit() and len(str(col).strip()) == 4:
            year_columns.append(col)
    except:
        continue

print(f"   Found {len(year_columns)} year columns")

# 3. Clean ONLY the year columns
print("\n3. Cleaning year columns (removing commas from numbers)...")

for col in year_columns:
    # Remove commas and convert to numeric
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '', regex=False), errors='coerce')
    # Count how many were cleaned
    cleaned_count = df[col].astype(str).str.contains(',').sum()
    if cleaned_count == 0:
        print(f"   ✅ {col}: Clean")
    else:
        print(f"   ✅ {col}: Fixed {cleaned_count} values")

# 4. Save cleaned file
output_file = 'gdp_cleaned_fixed.csv'
df.to_csv(output_file, index=False)
print(f"\n4. Saved cleaned file as '{output_file}'")

# 5. Show sample
print("\n5. Sample of cleaned data (first 3 countries):")
sample_cols = ['Country Name', 'Country Code', '1960', '1961', '1962']
if len(df) > 0:
    print(df[sample_cols].head(3).to_string())
else:
    print("   No data to display")

print("\n" + "="*50)
print("✅ CLEANING COMPLETE!")
print("="*50)
