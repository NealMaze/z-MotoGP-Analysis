# imports
from HelpersVer3 import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")
dest = ("C:/Users/LuciusFish/Desktop/csv/")

yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]

finFiles = []

for yr in yrs:
    rcFiles = getRacAnFiles(yr, dir)

    f = 3
    for file in rcFiles[f-1:f]: ####################################################################################
        print(file)
        g = file.replace(".pdf", ".csv")
        h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")

        rows, date = parsePDF(file)
        const = getConst(yr, h, date)

        mat = getMatrix(rows, const)

        # z = dest + h
        #
        # finFiles.append(h)
        # saveCSV(mat, z)
        # saveCSV(finFiles, "done")

