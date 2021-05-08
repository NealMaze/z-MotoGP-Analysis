# imports
from os import listdir, mkdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import os
import sys
from time import sleep
from winsound import Beep

def mkGoalDirs():
    try:
        types = ["RAC", "RAC2", "Q2", "Q1", "WUP", "FP1", "FP2", "FP3", "FP4"]
        desk = ("C:/Users/LuciusFish/Desktop/")
        one = "csv"
        path = os.path.join(desk, one)
        os.mkdir(path)
        for i in types:
            deskOne = f"{desk}{one}/"
            path = os.path.join(deskOne, i)
            os.mkdir(path)
    except:
        directories ="already made"

def getRacAnFiles(yr, dir, sesType):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*{sesType}*nalysis.pdf")
    rcFiles = [f"{dir}/{file}" for file in filter_files]

    return rcFiles

def parsePDF(rcFile, yr, h, file):
    col, date = openPDF(rcFile)
    rows = []
    const = getConst(yr, h, date)
    counter = 0

    while len(col) != 0:
        ty = len(col)
        row = runRow(col, const, file)
        if row != []:
            rows.append(row)
        elif len(col) == ty:
            counter += 1
            if counter == 5:
                sys.exit()
    return rows

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
    nonDis = ["*", "P", "Full"]
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

def getConst(yr, file, date):
    r = file.replace(f"{yr}-", "")
    o = r.replace(".csv", "")
    u = o.split("-")
    const = date
    for i in u[:4]:
        const.insert(0, i)

    return const

def runRow(lis, const, file):
    row = []

    longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    slowSpeed = re.compile("^\d\d[.]\d$")

    # try:
    if len(lis) == 0:
        row = []

    elif lis[0] == "unfinished" or lis[0] == "PIT":
        row = getBLap(lis)

    elif re.match(lapTime, lis[1]) or \
        re.match(longLap, lis[1]):
        row = getGLap(lis)

    else:
        row = getStats(lis)
        rowAddConst(row, const)

    # except:
    #     print(f"bad file: {file}")
    #     badSave(file)

    print(row)
    return row

def getRider(row):
    r = []
    tooMany = 0
    for i in row:
        r.append(i)

    rider = ["-number-", "-f_name-", "-l_name-", "-manufacturer-", "-nation-",
             "-team-", "-t_laps-", "-runs-", "-f_Tyre-", "-r_Tyre-",
             "-f_Age-", "-r_Age-", "-extra-"]

    if r[-1] == "Tyre":
        rider[11] = r[-2]
        del r[-2:]
        if r[-1] == "Tyre":
            rider[10] = r[-2]
            del r[-2:]

    x = 0
    trash = ["MotoGP", "Tyre", "Moto2", "Moto3"]
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    nations = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
               "AUT", "ARG", "CZE", "TUR"]
    manufacturers = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA"]

    while x < len(r):
        if tooMany == 500:
            print("too many in getRider(1)")
        tooMany += 1
        if r[x] in trash:
            del r[x]
        elif re.match(position, r[x]):
            del r[x]
        elif r[x] == "Total":
            strLaps = r[x+1]
            laps = strLaps.replace("laps=", "")
            rider[6] = laps
            del r[x:x+3]
        elif r[x] in nations:
            rider[4] = r[x]
            del r[x]
        elif r[x] == "Run":
            rider[7] = r[x+2]
            del r[x:x+3]
        elif r[x] in manufacturers:
            rider[3] = r[x]
            del r[x]
        else:
            x += 1

    x = 0
    while x < len(r):
        if tooMany == 500:
            print("too many in getRider(2)")
        tooMany += 1
        if re.match("^\d{1,2}$", r[x]):
            rider[0] = r[x]
            del r[x]
        elif r[x] == "Front":
            rider[8] = r[x+1]
            del r[x:x+2]
        elif r[x] == "Rear":
            rider[9] = r[x+1]
            del r[x:x+2]
        else:
            x += 1

    str = ""
    for i in r:
        str += f" {i}"

    rider[-1] = str

    return rider

def rowAddConst(row, const):
    for i in const:
        row.insert(0, i)

def getMatrix(rows, yr):
    matrix = []
    rider = ["none"]

    for row in rows:
        if row[0] == yr:
            rider = row
        else:
            lap = []
            for i in rider[:-1]:
                lap.append(i)
            for i in row:
                lap.append(i)
            lap.append(rider[-1])
            matrix.append(lap)

    return matrix

def saveCSV(mat, file):
    df = pd.DataFrame(mat)
    df.to_csv(file, index=False)

def badSave(file):
    badFiles = []
    dest = "C:/Users/LuciusFish/Desktop/csv/mistakenFiles.csv"

    with open(dest) as saveFile:
        contents = saveFile.readlines()
        for line in contents:
            x = line
            badFiles.append(x)

    del badFiles[0]

    badFiles.append(file)
    saveCSV(badFiles, dest)

def goodSave(file):
    finFiles = []
    dest = "C:/Users/LuciusFish/Desktop/csv/finishedFiles.csv"

    with open(dest) as saveFile:
        contents = saveFile.readlines()
        for line in contents:
            x = line
            finFiles.append(x)
    finFiles.append(file)

    del finFiles[0]

    saveCSV(finFiles, dest)

def intSaveFiles():
    try:
        finFiles = []
        badFiles = []

        with open(save) as saveFile:
            contents = saveFile.readlines()
            for line in contents:
                x = line[:-1]
                finFiles.append(x)

        with open(dest) as bFile:
            contents = bFile.readlines()
            for line in contents:
                x = line
                badFiles.append(x)
        good = "C:/Users/LuciusFish/Desktop/csv/finishedFiles.csv"
        bad = "C:/Users/LuciusFish/Desktop/csv/mistakenFiles.csv"

        saveCSV(finFiles, good)
        saveCSV(badFiles, bad)

    except:
        finFiles = []
        badFiles = []
        good = "C:/Users/LuciusFish/Desktop/csv/finishedFiles.csv"
        bad = "C:/Users/LuciusFish/Desktop/csv/mistakenFiles.csv"
        saveCSV(finFiles, good)
        saveCSV(badFiles, bad)

    return finFiles

def getGLap(lis):
    row = []
    longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    slowSpeed = re.compile("^\d\d[.]\d$")

    row.append(lis[0])
    del lis[0]
    row.append(lis[0])
    del lis[0]
    while True:
        if re.match(avgSpeed, lis[0]) or \
            re.match(slowSpeed, lis[0]):
            row.append(lis[0])
            del lis[0]
            break
        if len(lis) > 2:
            if re.match(lapTime, lis[2]) or \
                re.match(longLap, lis[2]):
                row.append(lis[0])
                del lis[0]
                break
        row.append(lis[0])
        del lis[0]

    lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for i in lapLength:
        if len(row) < i:
            row.insert(-1, f"Tsec{i - 3}")

    return row

def getBLap(lis):
    row = []
    longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    slowSpeed = re.compile("^\d\d[.]\d$")

    row.append("dnf")
    while True:
        if len(lis) == 0:
            break
        if re.match(avgSpeed, lis[0]) or \
            re.match(slowSpeed, lis[0]):
            row.append(lis[0])
            del lis[0]
            break
        else:
            row.append(lis[0])
            del lis[0]

    lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    for i in lapLength:
        if len(row) < i:
            row.insert(-1, f"Tsec{i - 3}")

    return row

def getStats(lis):
    low = []
    longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    slowSpeed = re.compile("^\d\d[.]\d$")

    low.append("Tyre")
    while True:
        if re.match(lapTime, lis[1]) or \
                lis[0] == "PIT" or \
                lis[0] == "unfinished" or \
                re.match(longLap, lis[1]):
            break
        else:
            low.append(lis[0])
            del lis[0]
    row = getRider(low)

    return row