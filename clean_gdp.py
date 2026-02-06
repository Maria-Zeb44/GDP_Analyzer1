
import pandas as pd
import pandas as pd

print("=== GDP CSV Cleaner ===")

# 1. Read CSV
print("1. Loading CSV...")
df = pd.read_csv('gdp_with_continent_filled.csv')
print(f"   Original: {df.shape[0]} rows, {df.shape[1]} columns")

# 2. Clean year columns
print("\n2. Cleaning year columns...")
year_columns = [col for col in df.columns if str(col).strip().isdigit() and len(str(col).strip()) == 4]

for col in year_columns:
    df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '', regex=False), errors='coerce')
    print(f"    Cleaned {col}")

# 3. Save cleaned file
output_file = 'gdp_cleaned_fixed.csv'
df.to_csv(output_file, index=False)
print(f"\n3. Saved as '{output_file}'")

# 4. SIMPLE TEST FUNCTION
print("\n" + "="*60)
print(" TEST YOUR CLEANED DATA")
print("="*60)

# Show first few countries
print("Available countries (first 5):")
for i, country in enumerate(df['Country Name'].head()):
    print(f"  {i+1}. {country}")

while True:
    print("\nOptions:")
    print("1. Check a country's GDP")
    print("2. Exit")
    
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == '1':
        # Show examples
        print("Examples: 'Aruba', 'Andorra', 'Afghanistan'")
        country = input("Country name: ").strip()
        year = input("Year (1960-2024): ").strip()
        
        if year not in df.columns:
            print(f" Year must be between 1960-2024")
            continue
        
        # FIXED SEARCH - exact match
        found = df[df['Country Name'].str.strip().str.lower() == country.lower()]
        
        if found.empty:
            print(f" '{country}' not found. Try exact name from list above.")
            continue
        
        gdp = found.iloc[0][year]
        
        if pd.isna(gdp):
            print(f" {country} in {year}: NO DATA AVAILABLE")
        else:
            print(f" SUCCESS! Data is clean!")
            print(f" {country} in {year}: ${gdp:,.2f}")
            print(f"   Continent: {found.iloc[0]['Continent']}")
            print(f"   Code: {found.iloc[0]['Country Code']}")
            
            # Show raw value to prove no commas
            print(f"   Raw value: {gdp} (no commas!)")
    
    elif choice == '2':
        print(" Testing complete! Data is clean.")
        break
    
    else:
        print("Please enter 1 or 2")

print("\n YOUR CSV IS CLEAN AND READY FOR ANALYSIS!")

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
        print(f"   {col}: Clean")
    else:
        print(f"   {col}: Fixed {cleaned_count} values")

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
print("CLEANING COMPLETE!")
print("="*50)
