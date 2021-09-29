# imports
from retrieveHelpers import *

print("\nData Retrieval System")
print("Step 1 - PDF Retrieval")
print(" select year to retrieve files from")
print(" entry can be between 1998-2021 or 'all'")
print("    *note: 'all' function not yet tested")

# get year from user
yr = "x"
yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008",
       "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998", "all"]

while yr not in yrs:
    print("\nplease enter a year between 1998-2021 or 'all'")
    yr = input("retrieve files from year: ")

if yr != "all":
    inRnd = input("enter numerals of requested rounds, separated by a comma\nretrieve files from rounds: ")
    rnds = inRnd.split(",")
    if rnds[0] == "all": rnds = "all"
else: rnds = "all"

# rewrite the getFiles(yr) function to take a round argument
grabFiles(yr, rnds)

# get testing files
   ###  GET TESTING FILES  ###

# convert PDFs to CSVs
print(f"\nConverting {yr} pdf files into csv files")
convertYrPdfs(yr)
print("converted")

