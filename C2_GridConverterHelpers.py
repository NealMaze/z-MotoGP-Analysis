# import necessary modules
from lists import *
from B2_ConverterHelpers import *

rnds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38",
        "39", "40", "41", "42", "43", "44", "45", "46", "47", "48", "49", "50"]

def openGridPDF(grdFile):
    # opens the pdf as a list of dictionaries and also returns the date for the session
    with plumb.open(grdFile) as pdf:
        pages = pdf.pages
        for pg in pages[:1]:
            sheet = pg.extract_words()
    return sheet

def stripHeader(page):
    x = 0
    y = [page[x-2]["text"], page[x-1]["text"], page[x]["text"]]
    z = ["Gap", "Top", "Speed"]

    while y != z:
        x = x + 1
        y = [page[x - 2]["text"], page[x - 1]["text"], page[x]["text"]]

    nuPage = page[x + 1:]
    return nuPage

def stripFooter(page):
    nuPage = []
    for row in page:
        if row[0] in rnds:
            nuPage.append(row)

    return nuPage

def getRows(page):
    nuPage = []
    row = []

    val = float(page[0]["top"])
    upper = val + 5
    lower = val - 5

    while len(page) != 0:
        if page[0]["top"] < upper and page[0]["top"] > lower:
            row.append(page[0]["text"])
            page.pop(0)
        else:
            nuPage.append(row)
            row = []

            val = float(page[0]["top"])
            upper = val + 5
            lower = val - 5

    return(nuPage)

def stripExtra(page):
    rows = []

    for row in page:
        nuRow = row[:4]
        rows.append(nuRow)

    return rows

def lowerCase(page):
    rows = []

    for row in page:
        nuRow = []
        for item in row:
            item = str(item)
            item = item.lower()
            nuRow.append(item)
        rows.append(nuRow)

    return rows

def convertGrid(yr, rnds):
    for lge in lges:
        print(f"{lge}")
        for rnd in rnds:
            grdFiles3 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*EP_Session.pdf")
            grdFiles2 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*QP_Session.pdf")
            grdFiles = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*QualifyingResults.pdf")
            for file in grdFiles2: grdFiles.append(file)
            for file in grdFiles3: grdFiles.append(file)

            if len(grdFiles) > 1:
                print("\n\n\nProblem")
                for i in grdFiles:
                    print(i)
                print("\n\n\n")

            for file in grdFiles:
                xFile = file.replace(pdfDir, "")
                print(xFile)
                fileName = file.replace(pdfDir, "")
                saveName = f"{yr}-{lge}-Round_{rnd}-StartGrid.csv"

                page = openGridPDF(file)
                page = stripHeader(page)
                page = getRows(page)
                page = stripFooter(page)
                page = stripExtra(page)
                page = lowerCase(page)

                for row in page:
                    row.insert(0, rnd)

                headers = ["rnd", "pos", "rdr_num", "f_name", "l_name"]

                saveCSV(page, f"{csvGridDir}{saveName}", headers)
