import csv 
with open('gdp_with_continent_filled.csv', mode='r') as file:
    csvFile=csv.reader(file)
    for lines in csvFile:
        print(lines)