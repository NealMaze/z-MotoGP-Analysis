# imports
from HelpersVer3 import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")
dest = ("C:/Users/LuciusFish/Desktop/csv/")

yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]

finFiles = []

for yr in yrs[:1]:
    rcFiles = getRacAnFiles(yr, dir)

    for file in rcFiles[1:2]:
        print(file)
        g = file.replace(".pdf", ".csv")
        h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")

        rows = parsePDF(file, yr, h)

        matrix = getMatrix(rows, yr)

        for i in matrix:
            print(i)

        z = dest + h
        a = dest + "finFiles.csv"

        finFiles.append(h)
        saveCSV(mat, z)
        saveCSV(finFiles, a)

