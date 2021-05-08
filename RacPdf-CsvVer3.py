# imports
from HelpersVer3 import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")
yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014",
       "2013", "2012", "2011", "2010"]
types = ["RAC", "RAC2", "Q2", "Q1", "WUP", "FP1", "FP2", "FP3", "FP4"]

mkGoalDirs()

finFiles = []
with open("C:/Users/LuciusFish/Desktop/csv/finFiles.txt", "r") as f:
    contents = f.readlines()
    for i in contents:
        finFiles.append(i)

for i in finFiles:
    if i == 0 or i ==[]:
        del i

print("finished files:")
for i in finFiles:
    print(i)
print("")

for sesType in types:
    dest = (f"C:/Users/LuciusFish/Desktop/csv/{sesType}/")

    for yr in yrs:
        rcFiles = getRacAnFiles(yr, dir, "RAC")
        print(f"{yr}, {sesType}")

        for file in rcFiles:
            if file not in finFiles:
                g = file.replace(".pdf", ".csv")
                h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")
                print(h)
                z = dest + h

                rows = parsePDF(file, yr, h, file)
                matrix = getMatrix(rows, yr)
                saveCSV(matrix, z)

                frequency = 500
                duration = 300
                Beep(frequency, duration)
                finFiles.append(file)
                with open("C:/Users/LuciusFish/Desktop/csv/finFiles.txt", "w") as f:
                    for i in finFiles:
                        f.write(i)

                del rows
                del matrix