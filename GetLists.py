# imports
from B2_ConverterHelpers import *
from GenGetters import *

dir = ("C:/Users/LuciusFish/Desktop/motoFiles/moto_pdf/Not")
cats = getListFile("cats")
manus = getListFile("manus")
nats = getListFile("nats")
rdrs = getListFile("rdrs")
tms = getListFile("tms")
yrs = getListFile("yrs")
lges = getListFile("lges")
print(cats)

for cat in cats:

    # for yr in yrs:
    files = getAnalyFiles(2020, dir, "*grid")
    #     # print(f"{yr}, {cat}")
    #
    #     if yr == 2021:
    #
    for file in files:

        with plumb.open(file) as pdf:
            whole = []
            pages = pdf.pages
            date = getDate(pages)
            for pg in pages:
                sheet = pg.extract_words()
                for i in sheet:
                    whole.append(i)

        for i in whole:
            print(i)

        # if "Round_1" in file:
        #     g = file.replace(".pdf", ".csv")
        #     h = g.replace("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis/", "")
        #     print(f"{cat}")
        #     z = dest + h
        #     col, date = openPDF(file)
        #
        #     for i in col[:5]:
        #         print(i)
        #     print("\n##################################################################################\n")

            # const = getConst(yr, h, date)
            #
            # ridLoq = getRidLoq(lis)
            #
            # rows = parsePDF(col)
            # matrix = getMatrix(rows, yr)
            # saveCSV(matrix, z)
            #
            # frequency = 500
            # duration = 300
            # Beep(frequency, duration)
            # finFiles.append(file)
            # with open("C:/Users/LuciusFish/Desktop/csv/finFiles.txt", "w") as f:
            #     for i in finFiles:
            #         f.write(i)
            #
            # del rows
            # del matrix

            exit()