# imports
from B2_ConverterHelpers import *

# with open(f"{sveDir}csvFinFiles.txt", "r") as f:
#     finFiles = []
#     contents = f.readlines()
#     for i in contents:
#         finFiles.append(i)
# for i in finFiles:
#     if i == 0 or i == []:
#         del i

nameColumn = []

# for i in finFiles:
#     print(i)
loqs = ["115.320", "376.080", "114.840", "375.600", "236.534", "497.284", ""]

xq = []
intColumn = []

for yr in yrs[:-8]:
    print(yr)
    print(len(xq))
    fNameColumn = []
    for lge in lges[:]:
        for sesType in ses[:]:
        #     with open(f"{csvDir}{yr}_Riders.csv", "r", encoding = "utf8") as yrFile:
        #         competitors = []
        #         i = csv.reader(yrFile, delimiter = ",")
        #         for r in i:
        #             competitors.append(r)
        #         for i in competitors:
        #             i[3] = i[3].split()
        #         del competitors[0]
        #         rdrNames = []
        #         for i in competitors:
        #             namE = str(i[3])
        #             namE2 = namE.split()
        #             fnamE = namE2[0]
        #             rdrNames.append(fnamE)
        #
            rcFiles = getAnalyFiles(pdfDir, f"{yr}*{lge}*{sesType}*nalysis.pdf")

            for file in rcFiles[:]:
                print(file)
                g = file.replace(".pdf", ".csv")
                h = g.replace("C:/Users/LuciusFish/Desktop/motoFiles/Analysis/", "")
                z = csvDir + h
                col, date = openPDF(file)
                # for row in col:
                #     value = row["text"]
                #     loc = row["x0"]
                #
                #
                #
                #     # if loc in loqs:
                #     #     if value not in rdrNames:
                #     #         print(value)
                #     #         print(loc)
                #     #         print("")
                #
                #
                #
                #     for i in competitors:
                #         try:
                #             xList = list(range(27,100))
                #             # if value == i[3][0] and value != "Marc":
                #             #     if loc not in fNameColumn:
                #             #         if yr not in fNameColumn:
                #             #             fNameColumn.append("")
                #             #             fNameColumn.append(yr)
                #             #         fNameColumn.append(value)
                #             #         fNameColumn.append(loc)
                for i in col:
                    value = i["text"]
                    loq = i["x0"]

                    iq = []
                    iq.append(yr)
                    iq.append(value)
                    iq.append(loq)

                    try:
                        int(value)
                        if loq not in intColumn:
                            intColumn.append(loq)
                            xq.append(iq)


                    except: lmnop = 0

print("################################################################################################################")
print("################################################################################################################")
print("################################################################################################################")
print("################################################################################################################")
print("################################################################################################################")


for i in xq:
    print(i)
print("")


                    # rows = parsePDF(col)
    # nameColumn.append(fNameColumn)



# for i in nameColumn:
#     print(i)