# imports
from os import listdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import sys

def getConst(yr, file, date):
    r = file.replace(f"{yr}-", "")
    o = r.replace(".csv", "")
    u = o.split("-")
    const = date
    const.append(u[0])
    const.append(u[1])
    const.append(u[2])
    const.append(u[3])

    return const

def getRacAnFiles(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rcFiles = [f"{dir}/{file}" for file in filter_files]
    return rcFiles

def parsePDF(rcFile):
    col, date = openPDF(rcFile)
    rows = []

    while len(col) != 0:
        row = runRow(col)
        rows.append(row)

    return rows, date

def openPDF(rcFile):
    with plumb.open(rcFile) as pdf:
        whole = []
        pages = pdf.pages
        date = getDate(pages)
        for pg in pages:
            sheet = pg.extract_words()
            col = stripBoilerPlate(sheet)
            for i in col:
                whole.append(i)

    return whole, date

def getDate(pages):
    words = pages[0].extract_words()
    date = []

    year = words[-5]["text"]
    day = words[-6]["text"]
    month = words[-7]["text"]

    x = f"{month} {day}"
    date.append(x)
    date.append(year)

    return date

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

    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")

    if lis[0] == "unfinished" or lis[0] == "PIT":
        row = []
        row.append("dnf")
        while True:
            row.append(lis[0])
            del lis[0]
            if re.match(avgSpeed, lis[0]):
                row.append(lis[0])
                del lis[0]
                break

    elif re.match(lapTime, lis[1]):
        while True:
            row.append(lis[0])
            del lis[0]
            if re.match(avgSpeed, lis[0]):
                row.append(lis[0])
                del lis[0]
                break

    else:
        row.append("Tyre")
        while True:
            row.append(lis[0])
            if len(row) == 40:
                for i in row:
                    print(f"too long rider row: {i}")

            del lis[0]
            lt = lis[1]
            if re.match(lapTime, lt):
                break

    return row

def getMatrix(rows, const):
    matrix = []
    rider = []
    head = []
    tempRider = {"Number": "none", "First_Name": "none", "Last_Name": "none", "Manufacturer": "none", "Nation": "none",
                 "Team": "none",
                 "Total_Laps": "none", "Run_#": "none", "Front_Tyre": "none", "Rear_Tyre": "none",
                 "Front_Tyre_Age": "none",
                 "Rear_Tyre_Age": "none"}

    while len(rows) != 0:
        for row in rows[:1]:#####################################################################################################
            if row[0] == "Tyre":
                rider = getRider(row)
                head = getHead(const, rider)
                del row[0]
            # else:
            #     lap = getLap(head, row[0])
            #     matrix.append(lap)
            #     del row[0]

    return matrix

def getRider(row):
    r = []
    for i in row:
        r.append(i)

    rider = {"Number": "none", "First_Name": "none", "Last_Name": "none", "Manufacturer": "none", "Nation": "none",
             "Team": "none", "Total_Laps": "none", "Run_#": "none", "Front_Tyre": "none", "Rear_Tyre": "none",
             "Front_Tyre_Age": "none", "Rear_Tyre_Age": "none"}

    if r[-1] == "Tyre":
        rider["Rear_Tyre_Age"] = r[-2]
        del r[-2:]
        if r[-1] == "Tyre":
            rider["Front_Tyre_Age"] = r[-2]
            del r[-2:]

    x = 0
    trash = ["MotoGP", "Tyre", "Moto2", "Moto3"]
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    nations = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
               "AUT", "ARG", "CZE", "TUR"]
    manufacturers = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA"]

    while x < len(r):
        if r[x] in trash:
            del r[x]
        elif re.match(position, r[x]):
            del r[x]
        elif r[x] == "Total":
            strLaps = r[x+1]
            laps = strLaps.replace("laps=", "")
            rider["Total_Laps"] = laps
            del r[x:x+3]
        elif r[x] in nations:
            rider["Nation"] = r[x]
            del r[x]
        elif r[x] == "Run":
            rider["Run_#"] = r[x+2]
            del r[x:x+3]
        elif r[x] in manufacturers:
            rider["Manufacturer"] = r[x]
            del r[x]
        else:
            x += 1

    x = 0
    while x < len(r):
        if re.match("^\d{1,2}$", r[x]):
            rider["Number"] = r[x]
            del r[x]
        elif r[x] == "Front":
            rider["Front_Tyre"] = r[x+1]
            del r[x:x+2]
        elif r[x] == "Rear":
            rider["Rear_Tyre"] = r[x+1]
            del r[x:x+2]
        else:
            x += 1

    return rider

def getHead(const, rider):
    r = const













jjj































