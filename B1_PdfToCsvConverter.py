# imports
from B2_ConverterHelpers import *

yrs = ["2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]
# lges = ["250cc"]
# rnd = "3"

for yr in yrs:
    for lge in lges:
        rcFiles = getFileNames(pdfDir, f"{yr}*Round_{rnd}-*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in rcFiles:
            for i in ses:
                if i in file:
                    sesType = i

            sesType = sesType.replace("_", "")
            sesType = sesType.replace("RACE2", "RAC2")

            saveName, track, round = getSaveName(file, sesType)
            print(saveName.replace(csvDir, ""))
            col, date = openPDF(file)
            lRows = parsePDF(col)

            rows = []
            for row in lRows:
                if row[0] != "bad":
                    rows.append(row)

            const = ["const", yr, lge, round, sesType, date, track,]

            cRows = getCRows(rows, yr, lge)

            cRows = rMisLaps(cRows)

            for row in cRows:
                x = 0
                while x < len(row):
                    i = row[x]
                    j = str(i)
                    row[x] = j
                    x += 1

                if row[0] == "lap":
                    lapNum = chkLap(row, lapNum)
                elif row[0] == "rider":
                    lapNum = 0
                    chkRider(row, yr)
                elif row[0] == "run":
                    chkRun(row)
                else:
                    print("line 228")
                    exit()

            matrix = getMatrix(cRows, const)
            saveCSV(matrix, saveName)
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
            del matrix
