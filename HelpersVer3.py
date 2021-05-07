# imports
from os import listdir, mkdir()
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import sys

def getRacAnFiles(yr, dir, sesType):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*{sesType}*nalysis.pdf")
    rcFiles = [f"{dir}/{file}" for file in filter_files]

    return rcFiles

def parsePDF(rcFile, yr, h):
    col, date = openPDF(rcFile)
    rows = []
    const = getConst(yr, h, date)

    while len(col) != 0:
        row = runRow(col, const)
        rows.append(row)


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

def runRow(lis, const):
    row = []
    tooMany = 0

    lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")

    try:
        if lis[0] == "unfinished" or lis[0] == "PIT":
            row.append("dnf")
            while True:
                if tooMany == 500:
                    print("runRow1")
                tooMany += 1
                if re.match(avgSpeed, lis[0]):
                    row.append(lis[0])
                    del lis[0]
                    break
                else:
                    row.append(lis[0])
                    del lis[0]

        elif re.match(lapTime, lis[1]):
            while True:
                if tooMany == 500:
                    print("runRow2")
                tooMany += 1
                if re.match(avgSpeed, lis[0]):
                    row.append(lis[0])
                    del lis[0]
                    break
                else:
                    row.append(lis[0])
                    del lis[0]

        else:
            low = []
            low.append("Tyre")
            while True:
                if tooMany == 500:
                    print("runRow3")
                tooMany += 1
                if re.match(lapTime, lis[1]) or \
                    lis[0] == "PIT" or \
                    lis[0] == "unfinished":
                    break
                else:
                    low.append(lis[0])
                    del lis[0]
            row = getRider(low)
            rowAddConst(row, const)

        lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        for i in lapLength:
            if len(row) < i:
                row.insert(-1, f"Tsec{i-3}")
    except:
        lmnop = 7

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
            print("getRider")
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
            print("getRider 2")
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
