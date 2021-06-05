# imports
from B2_ConverterHelpers import *

#"2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010",

yrs = ["2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]
lges = ["250cc"]

for yr in yrs:
    for lge in lges:
        rcFiles = getAnalyFiles(pdfDir, f"{yr}*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in rcFiles:
            if "Round_14" in file:
                for i in ses:
                    if i in file:
                        sesType = i

                sesType = sesType.replace("_", "")
                sesType = sesType.replace("RACE2", "RAC2")

                saveName, track = getSaveName(file, sesType)
                col, date = openPDF(file)
                rows = parsePDF(col, yr)
                const = ["const", yr, date, lge, track, sesType]

                # print("")
                # print(file)
                print(saveName.replace(csvDir, ""))
                rows.insert(0, const)

                cRows = getCRows(rows, yr, lge, file)

                for row in cRows:
                    x = 0
                    while x < len(row):
                        i = row[x]
                        j = str(i)
                        row[x] = j
                        x += 1

                    if row[0] == "lap":
                        chkLap(row)
                    elif row[0] == "rider":
                        chkRider(row, yr)
                    elif row[0] == "run":
                        chkRun(row)
                    else:
                        print("line 228")
                        exit()

                # matrix = getMatrix(cRows, const)
                # saveCSV(matrix, saveName)
                # frequency = 500
                # duration = 300
                # Beep(frequency, duration)
                #
                # csvFinFiles.append(file)
                # with open(f"{sveDir}csvFinFiles.txt", "w") as f:
                #     for i in csvFinFiles:
                #         f.write(i + "\\n")

                del rows
                del cRows
                # del matrix





