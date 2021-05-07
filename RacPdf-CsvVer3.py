# imports
from HelpersVer3 import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")
dest = ("C:/Users/LuciusFish/Desktop/csv/")

yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010"]

save = f"{dest}finishedFiles.csv"

try:
    finFiles = []
    with open(save) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            finFiles.append(row)
except:
    finFiles = []

print("finished files: ")
for file in finFiles:
    print(file)
print("\n\nrunning files:")

for yr in yrs:
    rcFiles = getRacAnFiles(yr, dir)

    for file in rcFiles:
        if file not in finFiles:
            print(file)
            g = file.replace(".pdf", ".csv")
            h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")

            rows = parsePDF(file, yr, h)

            matrix = getMatrix(rows, yr)

            z = dest + h

            saveCSV(matrix, z)
            saveCSV(finFiles, save)
            finFiles.append(file)
