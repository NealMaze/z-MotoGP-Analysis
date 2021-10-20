# imports
from A1_retrieveHelpers import *

allYrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009",
          "2008", "2007", "2006"]
allRnds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
           "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36",
           "37", "38", "39"]

print("\n          Data Retrieval System")
print("          Step 1 - Set Parameters")

print("\ndo you wish to retrieve pdf session files?")
retrieveSesFilesBin = input("y/n: ")
if retrieveSesFilesBin == "y":
    print("\nfrom what year do you want to retrieve session files?")
    print('(separate different years with ", ")')
    retrieveSesFilesYr = input("year: ")
    print("\nwhat rounds do you want to retrieve session files?")
    print('(separate different rounds with ", ")')
    retrieveSesFilesRnd = input("rounds: ")

    if ", " in retrieveSesFilesYr: rSFYs = retrieveSesFilesYr.split(", ")
    elif retrieveSesFilesYr == "all":
        rSFYs = allYrs
    else: rSFYs = [retrieveSesFilesYr]

    if ", " in retrieveSesFilesRnd: rSFRs = retrieveSesFilesRnd.split(", ")
    elif retrieveSesFilesRnd == "all":
        rSFRs = allRnds
    else: rSFRs = [retrieveSesFilesRnd]

print("\ndo you wish to retrieve pdf testing files?")
print("(this program will retrieve all test files from given year)")
retrieveTestFilesBin = input("y/n: ")
if retrieveTestFilesBin == "y":
    print("\nfrom what year do you want to retrieve testing files?")
    print('(separate different years with ", ")')
    retrieveTestFilesYr = input("year: ")

    if ", " in retrieveTestFilesYr: rTFYs = retrieveTestFilesYr.split(", ")
    else: rTFYs = [retrieveTestFilesYr]

print("\ndo you wish to convert all pdf session files?")
convertSesFilesBin = input("y/n: ")

if convertSesFilesBin != "y":
    print("\ndo you wish to clean all csv session files?")
    cleanSesFilesBin = input("y/n: ")
else: cleanSesFilesBin = "y"

########################################################################################################################

# retrieve PDF files
if retrieveSesFilesBin == "y":
    print(""
          "\n          Step 2 - Session PDF Retrieval")
    for yr in rSFYs:
        for rnd in rSFRs:
            grabFiles(yr, rnd)
else: print("\n          Skipping Step 2 - Session PDF Retrieval")

# get testing files
if retrieveTestFilesBin == "y":
    print("\n\n          Step 3 - Test PDF Retrieval")
    for yr in rTFYs:
        print(f"getting test PDFs from {yr}")
        getTestFiles(yr)
else: print("\n          Skipping Step 3 - Test PDF Retrieval")

# convert PDFs to CSVs
if convertSesFilesBin == "y":
    print("\n          Step 4 - PDF Conversion")
    for yr in allYrs:
        print(f"Converting {yr} session analysis files into csv files")
        for rnd in allRnds:
            convertYrPdfs(yr, rnd)
    print("converted")
elif retrieveSesFilesBin == "y":
    print("\n          Step 4 - PDF Conversion")
    for yr in rSFYs:
        print(f"Converting {yr} session analysis files into csv files")
        for rnd in rSFRs:
            convertYrPdfs(yr, rnd)
else: print("\n          Skipping Step 4 - PDF Conversion")

# clean data
print("\n          Step 5 - Data Cleaning")
if cleanSesFilesBin == "y":
    for yr in allYrs:
        print(f"\nCleaning {yr} csv files")
        cleanData(yr, allRnds)
    print("cleaned")
else:
    for yr in rSFYs:
        print(f"cleaning {yr} session analysis files into csv files")
        cleanData(yr, rnds)
    print("cleaned")
