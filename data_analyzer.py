import csv

with open('gdp_with_continent_filled.csv', mode='r') as file:
    csvFile = csv.reader(file)
    header = next(csvFile)   # first row (column names)