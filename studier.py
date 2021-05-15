# imports
from B2_ConverterHelpers import *

with open(f"{sveDir}csvFinFiles.txt", "r") as f:
    finFiles = []
    contents = f.readlines()
    for i in contents:
        finFiles.append(i)
for i in finFiles:
    if i == 0 or i == []:
        del i

nameColumn = []

print("finished files:")
for i in finFiles:
    print(i)
print("\n")
loqs = ["115.320", "376.080", "114.840", "375.600", "236.534", "497.284", ""]

for yr in yrs[:]:
    fNameColumn = []
    print(yr)
    for lge in lges[:]:
        for sesType in ses[:]:
            with open(f"{csvDir}{yr}_Riders.csv", "r", encoding = "utf8") as yrFile:
                competitors = []
                i = csv.reader(yrFile, delimiter = ",")
                for r in i:
                    competitors.append(r)
                for i in competitors:
                    i[3] = i[3].split()
                del competitors[0]
                rdrNames = []
                for i in competitors:
                    namE = str(i[3])
                    namE2 = namE.split()
                    fnamE = namE2[0]
                    rdrNames.append(fnamE)

            rcFiles = getAnalyFiles(yr, pdfDir, f"{yr}*{lge}*{sesType}*nalysis.pdf")

            for file in rcFiles[:]:
                if file not in finFiles:
                    g = file.replace(".pdf", ".csv")
                    h = g.replace("C:/Users/LuciusFish/Desktop/motoFiles/Analysis/", "")
                    z = csvDir + h
                    col, date = openPDF(file)
                    for row in col:
                        value = row["text"]
                        loc = row["x0"]



                        if loc in loqs:
                            if value not in rdrNames:
                                print(value)
                                print(loc)
                                print("")



                        for i in competitors:
                            try:
                                if value == i[3][0] and value != "Marc":
                                    if loc not in fNameColumn:
                                        if yr not in fNameColumn:
                                            fNameColumn.append("")
                                            fNameColumn.append(yr)
                                        fNameColumn.append(value)
                                        fNameColumn.append(loc)
                                # if value in ints:
                                #     if loc not in intColumn:
                                #         intColumn.append(file)
                                #         intColumn.append(yr)
                                #         intColumn.append(value)
                                #         intColumn.append(loc)
                                #         intColumn.append("")

                            except:
                                lmnop = 0
                    # rows = parsePDF(col)
    nameColumn.append(fNameColumn)

# print("")
# for i in intColumn:
#     print(i)
# print("")

for i in nameColumn:
    print(i)