# imports
from os import listdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import sys

def getRacAnFiles(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rcFiles = [f"{dir}/{file}" for file in filter_files]
    return rcFiles

def parsePDF(rcFile):
    col, const = openPDF(rcFile)


    # for sheet in col:
    #     left = []
    #     right = []
    #     while len(sheet) != 0:
    #         col, row = runRow(sheet)
    #         if col == "L":
    #             left.append(row)
    #         elif col == "R":
    #             right.append(row)
    #
    #     columns.append(left)
    #     columns.append(right)
    #
    # for col in columns:
    #     for row in col:
    #         data.append(row)

    return data, const

def openPDF(rcFile):
    with plumb.open(rcFile) as pdf:
        whole = []
        pages = pdf.pages
        const = getSessConst(pages)
        for pg in pages:
            sheet = pg.extract_words()
            col = stripBoilerPlate(sheet)
            for i in col:
                whole.append(i)

    return whole, const

def getSessConst(pages):
    words = pages[0].extract_words()
    sess_const = []

    year = words[-5]["text"]
    day = words[-6]["text"]
    month = words[-7]["text"]

    date = f"{month} {day} {year}"
    sess_const.append(date)
    sess_const.append(year)
    TRK = words[9]["text"]
    sess_const.append(TRK)
    league = words[8]["text"]
    sess_const.append(league)
    session = words[14]["text"]
    sess_const.append(session)
    return sess_const

def stripBoilerPlate(lis):
    cols = []
    L = []
    R = []
    x = 0

    while "Speed" not in lis[x]["text"]:
        x += 1
    x += 1
    del lis[0:x]

    x = 0
    while "Speed" not in lis[x]["text"]:
        x += 1
    x += 1
    del lis[0:x]

    x = 0
    while "Fastest" not in lis[x]["text"]:
        x += 1
    del lis[x:]

    x = 0
    nonDis = ["*", "Full"]
    while x < len(lis):
        y = lis[x]["text"]
        if y in nonDis:
            del lis[x]
        elif "Runs=" in y:
            del lis[x]
        else:
            x += 1

    listicle = ["1st", "12", "Maverick", "VINALES", "Yamaha", "SPA", "Monster", "Energy", "MotoGP", "laps=22", "laps=20",
                "Run", "#", "1", "Front", "Tyre", "Slick-Soft", "Rear", "New", "2'02.839", "3.392", "3.081", "28.555",
                "31.811", "192.8"]

    listicle = ["Maverick", "Johann", "Fabio", "Alex", "Pol", "Jack", "Stefan"]

    x0 = []
    qr = 0

    while qr < 25:
        for i in lis:
            if i["x0"] < 500:
                if i["text"] in listicle:
                    if 322 > i["x0"] > 115:
                        print(i["text"])
                        print(i["x0"])
                        print("")
                        x0.append(i["x0"])
                        qr += 1

    for i in lis:
        iVal = float(i["x0"])
        if iVal < 175:
            L.append(i["text"])
        elif iVal > 174:
            R.append(i["text"])

    print("")
    # for i in x0:
    #     print(i)

    for i in R:
        L.append(i)

    return L














#

#

#
# def getSheets(pages):
#     sheets = []
#
#     for pg in pages:
#         words = pg.extract_words()
#         stripBoilerPlate(words)
#
#     return sheets
#
#
#
# def runRow(lis):
#     col = ""
#     val = ""
#     row = []
#
#     wNum = re.compile("^\d{1,2}$")
#     lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
#     secTime = re.compile("^\d\d[.]\d\d\d$")
#     avgSpeed = re.compile("^\d\d\d[.]\d$")
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#     rfName = re.compile("^[A-Z][a-zÀ-ÿ]+$")
#
#     bLap = ["unfinished", "PIT"]
#
#     tstTxt = lis[0]["text"]
#
#     while len(row) < 1:
#
#         if "Runs=" in tstTxt:
#             strLaps = lis[2]["text"]
#             row = strLaps.replace("laps=", "")
#             val = "lapsRun"
#             del lis[:5]
#
#         elif re.match(position, tstTxt):
#             row = getNumber(lis)
#             val = "num"
#
#         elif lis[0]["text"] in bLap:
#             row = getBadLap(lis)
#             val = "badlap"
#
#         elif re.match(wNum, tstTxt):
#             row = getGoodLap(lis)
#             val = "goodlap"
#
#         elif re.match(rfName, tstTxt):
#             row = getRider(lis)
#             val = "rider"
#
#         else:
#             print("row prob")
#             print(lis[0:10])
#             sys.exit()
#
#     print(f"{val} = {row}")
#     return col, row






































