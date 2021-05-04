# imports
from helpers import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")
dest = ("C:/Users/LuciusFish/Desktop/csv/")

yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]

finFiles = []

for yr in yrs:
    rcFiles = getRacAnalysis(yr, dir)

    for file in rcFiles:
        print(file)
        g = file.replace(".pdf", ".csv")
        h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")

        data, const = parsePDF(file)
        mat = getMatrix(data, const)

        z = dest + h

        finFiles.append(h)
        saveCSV(mat, z)
        saveCSV(finFiles, "done")