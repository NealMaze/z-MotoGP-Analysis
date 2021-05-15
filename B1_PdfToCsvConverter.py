# imports
from B2_ConverterHelpers import *

csvFinFiles = getFinFils("csv")

for yr in yrs:
    for lge in lges:


        rcFiles = getAnalyFiles(yr, dir, f"{yr}*{sesType}*nalysis.pdf")
        print(f"{yr}, {sesType}")

        for file in rcFiles:
            if file not in finFiles:
                g = file.replace(".pdf", ".csv")
                h = g.replace(f"{pdfFiles}", "")
                print(h)
                z = dest + h
                col, date = openPDF(file)

                rows = parsePDF(col)
                matrix = getMatrix(rows, yr)
                saveCSV(matrix, z)

                frequency = 500
                duration = 300
                Beep(frequency, duration)
                finFiles.append(file)
                with open(f"{sveFiles}csvFinFiles.txt", "w") as f:
                    for i in finFiles:
                        f.write(i)

                del rows
                del matrix