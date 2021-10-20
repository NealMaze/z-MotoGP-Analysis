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
        sheet = pages[0] .extract_words()
    return sheet

def stripHeader(page):
    x = 0
    y = page[x]["text"]

    while y != "Pos":
        x = x + 1
        y = page[x]["text"]

    nuPage = page[x:]
    return nuPage

def getPos(page):
    gridLis = []
    x = 0
    y = page[x]["text"]
    gridPos = page[x]["top"]

    while y != "Pos":
        x = x + 1
        y = page[x]["text"]
        if y == "Pos":
            gridPos = page[x]["top"]
            break

    val = float(gridPos)
    upper = val + 3
    lower = val - 3

    x = 0
    while upper > float(page[x]["top"]) > lower:
        gridLis.append(page[x]["text"])
        x = x + 1

    ngLis = []
    for x in gridLis:
        if len(x) < 3:
            ngLis.append(x)
        else:
            y = [x[j:j+2] for j in range(0, len(x), 2)]
            for item in y:
                ngLis.append(item)

    lenLis = len(ngLis)
    return lenLis, ngLis

def getNum(page):
    gridLis = []
    x = 0
    y = page[x]["text"]

    while y != "Grid":
        x = x + 1
        y = page[x]["text"]
        if y == "Grid":
            gridPos = page[x]["top"]
            break

    val = float(gridPos)
    upper = val + 5
    lower = val - 5

    x = 0
    for item in page:
        y = float(item["top"])
        if y < upper and y > lower:
            gridLis.append(item["text"])

    ngLis = []
    for x in gridLis:
        if len(x) < 3:
            ngLis.append(x)
        else:
            y = [x[j:j + 2] for j in range(0, len(x), 2)]
            for item in y:
                ngLis.append(item)

    lenLis = len(ngLis)
    return lenLis, ngLis
