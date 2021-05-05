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
    col, date = openPDF(rcFile)
    rows = []

    for i in col:
        print(i)

    # while len(col) != 0:
    #     row = runRow(col)
    #     rows.append(row)

    return rows, date

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

    date = f"{month} {day}"
    sess_const.append(date)
    sess_const.append(year)

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

    for i in lis:
        iVal = float(i["x0"])
        if iVal < 310:
            L.append(i["text"])
        elif iVal > 309:
            R.append(i["text"])

    for i in R:
        L.append(i)

    return L

def runRow(lis):
    row = []

    wNum = re.compile("^\d{1,2}$")
    lapTime = re.compile("^\d[']\d\d[.]\d\d\d")
    secTime = re.compile("^\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    rfName = re.compile("^[A-Z][a-zÀ-ÿ]+$")

    bLap = ["unfinished", "PIT"]

    if lis[0] in bLap:
        row = []
        row.append("dnf")
        while re.match(avgSpeed, lis[0]):
            row.append(lis[0])

    elif (
        re.match(wNum, lis[0]) and
        re.match(lapTime, lis[1]) and
        re.match(secTime, lis[2]) and
        re.match(secTime, lis[3]) and
        re.match(secTime, lis[4]) and
        re.match(secTime, lis[5]) and
        re.match(avgSpeed, lis[6])
    ):
        row = []
        for i in lis[:7]:
            row.append(i)
        del lis[:7]


    else:
        row = getRider(lis)
    return row

def getRider(lis):
    










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







































