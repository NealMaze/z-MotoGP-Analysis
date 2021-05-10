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
    positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
                 "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
                 "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]

    sheets = []

    for pg in pages:
        words = pg.extract_words()
        stripBoilerPlate(words)

    return sheets

def runRow(lis):
    col = ""
    val = ""
    row = []

    lapCount = re.compile("^\d{1,2}$")
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






        elif re.match(lapCount, tstTxt):
            row = getGoodLap(lis)
            val = "goodlap"

        elif re.match(rfName, tstTxt):
            row = getRider(lis)
            val = "rider"
            print(f"{val} = {row}")
            
        else:
            print("row prob")
            print(lis[0:10])
            sys.exit()


    return col, row

# def runRow(lis):
#     col = ""
#     val = ""
#     row = []
#
#     lapCount = re.compile("^\d{1,2}")
#     lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
#     sectionTime = re.compile("^\d\d[.]\d\d\d$")
#     avgSpeed = re.compile("^\d\d\d[.]\d$")
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#     rfName = re.compile("^[A-Z][a-zÀ-ÿ]+$")
#
#     positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
#                  "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
#                  "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]
#     lapList = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
#             "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
#             "39", "40"]
#     bLap = ["unfinished", "PIT"]
#
#     tstTxt = lis[0]["text"]
#
#     while len(row) < 1:
#         lisVal = float(lis[0]["x0"])
#         if lisVal < 175:
#             col = "L"
#         elif lisVal > 174:
#             col = "R"
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
#         elif re.match(lapCount, tstTxt):
#             row = getGoodLap(lis)
#             val = "goodlap"
#
#         elif re.match(rfName, tstTxt):
#             row = getRider(lis)
#             val = "rider"
#         else:
#             print("row prob")
#             print(lis[0])
#
#     print(f"{val} = {row}")
#     return col, row

def getRider(lis):
    rider = []
    rider.append("new")
    fName = lis[0]["text"]
    lName = lis[1]["text"]
    rider.append(fName)
    rider.append(lName)
    del lis[0:2]
    team, nat = getRiderTeam(lis)
    rider.append(team)
    rider.append(nat)

    return rider

def getRiderTeam(lis):
    nations = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
               "AUT", "ARG", "CZE", "TUR"]
    ls = []
    team = ""
    x = 0

    while lis[x]["text"] not in nations:
        ls.append(lis[x]["text"])
        x += 1
        if x == 10:
            print("missing nation code:")
            print(ls)
            print("\n\n")

    del lis[:x]
    nat = lis[0]["text"]
    for i in ls:
        j = f" {i}"
        team += j
    del lis[0]

    return team, nat

def getBadLap(lis):

    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    secTime = re.compile("^\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")

    lap = []
    lap.append("dnf")
    lap.append(lis[0]["text"])
    del lis[0]




########################################################################################################################



    z = 0
    while z == 0:
        x = lis[0]["text"]
        if re.match(lapTime, x):
            lap.append(lis[0]["text"])
            del lis[0]
        elif re.match(secTime, x):
            lap.append(lis[0]["text"])
            del lis[0]
        elif re.match(avgSpeed, x):
            lap.append(lis[0]["text"])
            del lis[0]
            z = 1
        else:
            z = 1








    # ls = []
    # x = 0
    # while x != 1:
    #     try:
    #         if float(lis[0]["text"]) > 100:
    #             lap.append(lis[0]["text"])
    #             x = 1
    #             print("try block")
    #             print(lis[0]["text"])
    #     except:
    #         lap.append(lis[0]["text"])
    #
    #
    # # while len(lap) < 8:
    # #     print(lap)
    # #     if lis[0]["text"] in lapList:
    # #         lap.append("none")
    # #     elif lis[0]["text"]
    # #
    # #     if lis[0]["text"] not in lapList:
    # #         lap.append(lis[0]["text"])
    # #         del lis[0]
    # #     else:
    # #         lap.append("none")
########################################################################################################################


    return lap

def getGoodLap(lis):
    lap = []

    if lis[2]["text"] == "P":
        del lis[2]
        lis[1]["text"] += " P"

    for i in lis[:7]:
        lap.append(i["text"])
    del lis[:7]

    return lap

def getNumber(lis):
    row = []
    pos = lis[0]["text"]
    num = lis[1]["text"]
    row.append(pos)
    row.append(num)

    del lis[:2]
    return row

def parsePDF(rcFile):
    sheets, const = openPDF(rcFile)
    columns = []
    data = []

    for sheet in sheets:
        left = []
        right = []
        while len(sheet) != 0:
            col, row = runRow(sheet)
            if col == "L":
                left.append(row)
            elif col == "R":
                right.append(row)

        columns.append(left)
        columns.append(right)

    for col in columns:
        for row in col:
            data.append(row)

    return data, const

def getHeader(data, const):
    head = []
    for i in const:
        head.append(i)
    for i in data[0]:
        head.append(i)
    del data[0]
    for i in data[0]:
        head.append(i)
    del data[0:2]
    del head[5]
    del head[9]

    return head

def getLap(head, row):
    lap = []
    for i in head:
        lap.append(i)
    for i in row:
        lap.append(i)

    return lap

def getMatrix(data, const):
    matrix = []

    while len(data) != 0:
        if data[0][0] == "new":
            head = getHeader(data, const)
        else:
            lap = getLap(head, data[0])
            matrix.append(lap)
            del data[0]

    return matrix

def saveCSV(mat, file):
    df = pd.DataFrame(mat)
    df.to_csv(file, index=False)








