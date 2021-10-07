# imports
from retrieveHelpers import *

print("\n          Data Retrieval System")
print("          Step 1 - Set Parameters")
# get year from user
yr = "x"
yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008",
       "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

while yr not in yrs:
    yr = input("\nplease enter a year from 1998 to the present from which to retrieve files\nretrieve files from year: ")
    if yr not in yrs: print("invalid selection\n")
inRnd = input('\nenter numerals of requested rounds, separated by \n'
              'a comma and a space, or request a range like "4-10"\nretrieve files from rounds: ')
testConf = input("\ndo you wish to retrieve testing data? (y/n): ")
uIn = input("do you wish to clean data in all seasons? (y/n): ")

print("          Step 2 - Session PDF Retrieval")
if ", " in inRnd:
    rnds = inRnd.split(", ")
else: rnds = [inRnd]

# retrieve PDF files
grabFiles(yr, rnds)

# get testing files
print("\n          Step 3 - Test PDF Retrieval")
if testConf == "y":
    print("getting test PDFs from year")
    getTestFiles(yr)

# convert PDFs to CSVs
print("\n          Step 4 - PDF Conversion")
print(f"Converting {yr} session analysis files into csv files")
convertYrPdfs(yr, rnds)
print("converted")

# convert grid files to CSVs
print("\n          Step 5 - Grid Conversion")
print(f"Converting {yr} qualifying files into csv files")
convertGrid
print("converted")

# clean data
print("\n          Step 6 - Data Cleaning")
print(f"Converting {yr} pdf files into csv files")
cleanData(uIn, yr)
print("cleaned")
