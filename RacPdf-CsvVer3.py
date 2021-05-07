# imports
from HelpersVer3 import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")

yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]

types = ["RAC", "Q2", "Q1", "WUP", "FP1", "FP2", "FP3", "FP4", ]

for sesType in types:
    try:
        finFiles = []
        with open(save) as saveFile:
            contents = saveFile.readlines()
            for line in contents:
                x = line[:-1]
                finFiles.append(x)

        del finFiles[0]
        print("finished files: ")
        for file in finFiles:
            print(file)
        print("\n\nrunning files:")
    except:
        finFiles = []

    dest = (f"C:/Users/LuciusFish/Desktop/csv/{sesType}/")
    save = f"{dest}finishedFiles.csv"

    for yr in yrs:
        rcFiles = getRacAnFiles(yr, dir, sesType)

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
