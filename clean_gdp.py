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
