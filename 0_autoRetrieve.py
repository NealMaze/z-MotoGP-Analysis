# imports
from retrieveHelpers import *

print("\n          Data Retrieval System")
print("          Step 1 - Session PDF Retrieval")

# get year from user
yr = "x"
yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008",
       "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

while yr not in yrs:
    yr = input("\nplease enter a year from 1998 to the present from which to retrieve files\nretrieve files from year: ")
    if yr not in yrs: print("invalid selection\n")

inRnd = input('\nenter numerals of requested rounds, separated by \n'
              'a comma and a space, or request a range like "4-10"\nretrieve files from rounds: ')

if ", " in inRnd:
    rnds = inRnd.split(", ")

else: rnds = [inRnd]

grabFiles(yr, rnds)

# get testing files

print("\n          Step 2 - Test PDF Retrieval")
testConf = input("do you wish to retrieve testing data? (y/n): ")
if testConf == "y":
    print("getting test PDFs from year")
    getTestFiles(yr)

# convert PDFs to CSVs
print("\n          Step 3 - PDF conversion")
print(f"\nConverting {yr} pdf files into csv files")
convertYrPdfs(yr)
print("converted")
