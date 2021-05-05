# imports
from os import listdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import sys

def getRacAnalysis(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rcFiles = [f"{dir}/{file}" for file in filter_files]
    return rcFiles

def stripBoilerPlate(lis):
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
    while x < len(lis):
        if lis[x]["text"] == "*":
            del lis[x]
        else:
            x += 1

def openPDF(rcFile):
    with plumb.open(rcFile) as pdf:
        sheets = []
        pages = pdf.pages
        const = getSessionConstants(pages)
        for pg in pages:
            sheet = pg.extract_words()
            stripBoilerPlate(sheet)
            sheets.append(sheet)

    return sheets, const

def getSessionConstants(pages):
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

def getSheets(pages):
    sheets = []

    for pg in pages:
        words = pg.extract_words()
        stripBoilerPlate(words)

    return sheets

def parsePDF(rcFile):
    sheets, const = openPDF(rcFile)
    columns = []
    data = []

    for sheet in sheets:
        for word in sheet:
            print(word["text"])

    # for sheet in sheets:
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

def runRow(lis):
    col = ""
    val = ""
    row = []

    wNum = re.compile("^\d{1,2}$")
    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    secTime = re.compile("^\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    rfName = re.compile("^[A-Z][a-zÀ-ÿ]+$")

    bLap = ["unfinished", "PIT"]

    tstTxt = lis[0]["text"]

    while len(row) < 1:
        lisVal = float(lis[0]["x0"])
        if lisVal < 175:
            col = "L"
        elif lisVal > 174:
            col = "R"


        if "Runs=" in tstTxt:
            strLaps = lis[2]["text"]
            row = strLaps.replace("laps=", "")
            val = "lapsRun"
            del lis[:5]

        elif re.match(position, tstTxt):
            row = getNumber(lis)
            val = "num"

        elif lis[0]["text"] in bLap:
            row = getBadLap(lis)
            val = "badlap"

        elif re.match(wNum, tstTxt):
            row = getGoodLap(lis)
            val = "goodlap"

        elif re.match(rfName, tstTxt):
            row = getRider(lis)
            val = "rider"

        else:
            print("row prob")
            print(lis[0:10])
            sys.exit()

    print(f"{val} = {row}")
    return col, row






































