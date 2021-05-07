# imports
from HelpersVer3 import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")
desk = ("C:/Users/LuciusFish/Desktop/")
one = "csv"
sessions = [""]
yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]
types = ["RAC", "RAC2" "Q2", "Q1", "WUP", "FP1", "FP2", "FP3", "FP4"]



for sesType in types:
    dest = (f"C:/Users/LuciusFish/Desktop/csv/{sesType}/")
    save = f"{dest}finishedFiles.csv"

    try:
        finFiles = []
        with open(save) as saveFile:
            contents = saveFile.readlines()
            for line in contents:
                x = line[:-1]
                finFiles.append(x)

        del finFiles[0]
        # print("finished files: ")
        # for file in finFiles:
        #     print(file)
        # print("\n\nrunning files:")
    except:
        finFiles = []

    for yr in yrs:
        print(f"{yr}, {sesType}")
        rcFiles = getRacAnFiles(yr, dir, sesType)
        fileCount = 0

        for file in rcFiles:
            if file not in finFiles:
                print(file)
                g = file.replace(".pdf", ".csv")
                h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")
                z = dest + h

                rows = parsePDF(file, yr, h)

                matrix = getMatrix(rows, yr)

                saveCSV(matrix, z)
                saveCSV(finFiles, save)
                finFiles.append(file)
                fileCount += 1
        print(f"Files Converted: {str(fileCount)}\n")