# imports
from os import listdir, mkdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import os
import csv
import sys
from GenGetters import *
from time import sleep
from winsound import Beep
from lists import *

def getFinFiles(type):
    finFiles = []
    with open(f"{sveDir}/{type}FinFiles.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            finFiles.append(i)

    for i in finFiles:
        if i == 0 or i == []:
            del i

    print("finished files:")
    if len(finFiles) == 0:
        print("none")
        y = finFiles
    else:
        y = finFiles[0].split("|")
        for i in y:
            print(i)

    return y

def getAnalyFiles(dir, string):
    filterFiles = fnmatch.filter(listdir(dir), f"{string}")
    files = [f"{dir}{file}" for file in filterFiles]

    return files

def getSaveName(file, sesType):
    y = file.replace(pdfDir, "")
    t = y.split("-")
    round = t[1]
    lge = t[2]
    track = t[4].strip()
    yr = t[0].replace("/", "")
    saveName = f"{yr}-{lge}-{round}-{track}-{sesType}-Analysis.csv"
    z = csvDir + saveName
    return z, track

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

    x = date[0].replace(",", "")

    return whole, x

def getDate(pages):
    # """Gets the date of the event and returns it to the openPDF() function"""

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
    nonDis = ["**", "*", "Full"]
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
            L.append(i)
        elif iVal > 309:
            R.append(i)

    for i in R:
        L.append(i)

    p = 0
    while len(L) > p:
        if L[p]["text"] == "Rear":
            del L[p]
        elif "Rear" in L[p]["text"]:
            x = L[p]["text"]
            y = x.replace("Rear", "")
            L[p]["text"] = y
        else:
            p += 1

    p = 0
    while len(L) > p:
        if L[p]["text"] == "Front":
            del L[p]
        elif "Front" in L[p]["text"]:
            x = L[p]["text"]
            y = x.replace("Rear", "")
            L[p]["text"] = y
        else:
            p += 1

    return L

def parsePDF(col, yr):
    rows = []
    counter = 0

    while len(col) != 0:
        catch = len(col)
        row = getRow(col, yr)
        if row != []:
            rows.append(row)


        if len(col) == catch:
            counter += 1
            if counter == 5:
                print("")
                print("looping")
                for row in rows[-5:]:
                    print(row)
                sys.exit()

    return rows

def getLap(lis):
    loq = lis[0]["top"]
    hi = loq + 1
    lo = loq - 1
    row = ["lap"]

    while True:
        if len(lis) == 0:
            break
        elif lis[0]["top"] > hi:
            break
        elif lis[0]["top"] < lo:
            break
        else:
            row.append(lis[0]["text"])
            del lis[0]

    return row

def getRow(lis, yr):
    val = "none"
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    name = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")

    if len(lis) < 1:
        print("empty row")
        row = []

    elif len(lis) < 2:
        print("line 177, helpers #####################################################################################################################################################################")
        print(lis[:10]["text"])
        exit()

    elif lis[0]["text"] == "unfinished" or lis[0]["text"] == "PIT":
        val = "lap"
        row = getLap(lis)

    elif re.match(lapTime, lis[1]["text"]):
        val = "lap"
        row = getLap(lis)

    elif lis[0]["text"] == "Run" or lis[0]["text"] == "Run#" or lis[0]["text"] == "run" or lis[0]["text"] == "run#":
        val = "run"
        row = getRun(lis)

    elif re.match(position, lis[0]["text"]) or re.match(name, lis[0]["text"]):
        val = "rider"
        low = getRiderRow(lis)
        row = formatRiderRow(low)
        rowAddRdrData(row, yr)

    else:
        print("")
        print(f" - - - {yr}, {lge}, {sesType} - - - ")
        print("Line 196 Helpers ###########################################################################################################################################")
        for i in line[:4]:
            print(f"{i}")
        print("##################################################################")

    x = row[0].lower()
    row[0] = x

    return row

def getRiderRow(lis):
    runs = ["Run", "run", "Run#", "run#"]
    row = []
    while True:
        row.append(lis[0]["text"])
        del lis[0]
        if len(lis) < 2:
            row.append(lis[0]["text"])
            del lis[0]
            break
        if lis[0]["text"] in runs:
            break

    return row

def formatRiderRow(row):
    rider = ["-0-number-", "-1-f_name-", "-2-l_name-", "-3-manufacturer-", "-4-nation-",
             "-5-team-", "-6-t_laps-", "-7-run_number-", "-8-f_Tire-", "-9-r_Tire-",
             "-10-f_Age-", "-11-r_Age-", "-12-extra-"]
    trash = ["MotoGP", "Tyre", "Moto2", "Moto3", "500cc", "125cc", "250cc"]
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")

    x = 0
    while x < len(row):
        val = row[x]
        if val in trash:
            del row[x]
        elif re.match(position, val):
            del row[x]
        elif val == "Total":
            strLaps = row[x+1]
            rider[6] = strLaps
            del row[x:x+3]
        elif val in nats:
            rider[4] = val
            del row[x]
        elif val == "Run":
            rider[7] = row[x+2]
            del row[x:x+3]
        elif val in manus:
            rider[3] = val
            del row[x]
        else:
            x += 1

    x = 0
    while x < len(row):
        val = row[x]
        if re.match("^\d{1,2}$", val) and rider[0] == "-0-number-":
            rider[0] = val
            del row[x]
        else:
            x += 1

    x = 0

    while x < len(row):
        val = row[x]
        if "Tyre" in val:
            row[x] = val.replace("Tyre", "")
        else:
            x += 1

    string = ""

    for i in row:
        val = i
        string += f" {val}"
    rider[-1] = string.strip()

    return rider

def rowAddRdrData(row, yr):
    rData = getRidersData(yr)
    found = False

    print("")
    rNum = row[0]
    rNat = row[4]
    rManu = row[3]
    print(row)

    while found == False:

        for i in rData:
            num = i[2]
            name = i[3]
            nat = i[4]
            team = i[5]
            m = i[6]
            manu = m.upper()

            if num == row[0]:
                print(i[2:])
                y = row[12].replace(name, "")
                row[12] = y.strip()
                x = name.split(" ", 1)
                row[1] = x[0]
                row[2] = x[1]
                row[5] = team
                found = True
    del row[12]
    row.insert(0, "rider")

def getRidersData(yr):
    data = []
    rows = []

    with open(f"{csvDir}{yr}_Riders.csv", "r", encoding="utf8") as yrFile:
        i = csv.reader(yrFile, delimiter=",")
        for r in i:
            if r[0] != "f":
                rows.append(r)
        del rows[0]
        q = []

    if len(rows[0]) < 3:
        for i in rows[0]:
            print(i)
            data.append(i)

    elif len(rows[0]) > 3:
        for row in rows:
            data.append(row)

    return data

def getRun(lis):
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d$")
    row = []
    while True:
        row.append(lis[0]["text"])
        del lis[0]
        if len(lis) < 2:
            row.append(lis[0]["text"])
            del lis[0]
            break
        elif re.match(lapTime, lis[1]["text"]):
            break
        elif lis[0]["text"] == "unfinished" or lis[0]["text"] == "PIT":
            break

    p = 0
    while p < len(row):
        q = str(row[p])
        listen = ["Tyre", "at", "start", "#", "data"]
        if q in listen:
            del row[p]
        elif "Tyre" in q:
            x = q.replace("Tyre", "")
            row[p] = x
            p += 1
        elif "Laps" in q:
            x = q.replace("Laps", "")
            row[p] = x
            p += 1
        elif q == "New":
            row[p] = "0"
            p += 1
        elif q == "**":
            row[p] = "missing"
            p += 1
        else: p += 1

    count = 0
    while count < len(row):
        val = row[count]
        if val == "":
            del row[count]
            row.insert(count, "missing")
        else:
            count += 1

    return row

def getMatrix(rows, const):
    matrix = []

    for row in rows:
        lap = []
        if row[0] == "rider":
            rider = []
            for i in const: rider.append(i)
            for i in row[1:]: rider.append(i)
        elif row[0] == "run":
            del rider[8:]
            for i in row[1:]: rider.append(i)
        elif row[0] == "lap":
            for i in rider: lap.append(i)
            for i in row[1:]: lap.append(i)
            matrix.append(lap)
        else:
            exit()

    return matrix

def saveCSV(mat, file):
    df = pd.DataFrame(mat)
    df.to_csv(file, index=False)

def fixRow(row):

    inte = re.compile("^\d{1,2}$")
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    name = re.compile(
        "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")
    secTime = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}$")
    avgSpeed = re.compile("^\d{2,3}[.]\d{1}$")

    tires = ["Slick-Soft", "Slick-Medium", "Slick-Hard", "Wet-Soft", "Wet-Medium", "Wet-Hard", "missing"]
    manus = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA", "KAWASAKI", "BMW", "TRIUMPH"]
    nats = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
            "AUT", "ARG", "CZE", "TUR"]

    if row[0] == "lap":
        if re.match(inte, row[1]) == None:
            row.insert(1, "dnf")
        if row[2] == "PIT":
            row[2] = "unfinished"
        if row[3] != "P":
            row.insert(3, "did not pit")
        else:
            row[3] = "pit"
        if re.match(avgSpeed, row[-1]) == None:
            row.append("missing speed")
        while len(row) != 13:
            row.insert(-1, "no section time")

    return row

def chekRows(rows, file):
    inte = re.compile("^\d{1,2}$")
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    name = re.compile(
        "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")
    secTime = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}$")
    avgSpeed = re.compile("^\d{2,3}[.]\d{1}$")

    tires = ["Slick-Soft", "Slick-Medium", "Slick-Hard", "Wet-Soft", "Wet-Medium", "Wet-Hard", "missing"]
    manus = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA", "KAWASAKI", "BMW", "TRIUMPH"]
    nats = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
            "AUT", "ARG", "CZE", "TUR"]

    for i in rows:
        if i[0] == "rider":
            if len(i) != 13: print(f"{file}\n{i}")
            if re.match(inte, i[1]) == None: print(f"{file}\n{i}")
            if re.match(name, i[2]) == None: print(f"{file}\n{i}")
            if re.match(name, i[3]) == None: print(f"{file}\n{i}")
            if i[4] not in manus: print(f"{file}\n{i}")
            if i[5] not in nats: print(f"{file}\n{i}")
            if "laps=" not in i[7] and i[7] != "-6-t_laps-" : print(f"{file}\n{i}")

            assert len(i) == 13
            assert re.match(inte, i[1])
            assert re.match(name, i[2])
            assert re.match(name, i[3])
            assert i[4] in manus
            assert i[5] in nats
            assert "laps=" in i[7] or i[7] == "-6-t_laps-"

        elif i[0] == "run":
            if len(i) != 6: print(f"{file}\n{i}")
            if re.match(inte, i[1]) == None: print(f"{file}\n{i}")
            if i[2] not in tires: print(f"{file}\n{i}")
            if i[3] not in tires: print(f"{file}\n{i}")
            if re.match(inte, i[4]) == None and i[4] != "missing": print(f"{file}\n{i}")
            if re.match(inte, i[5]) == None and i[4] != "missing": print(f"{file}\n{i}")

            assert len(i) == 6
            assert re.match(inte, i[1])
            assert i[2] in tires
            assert i[3] in tires
            assert re.match(inte, i[4]) or i[4] == "missing"
            assert re.match(inte, i[5]) or i[4] == "missing"

        elif i[0] == "lap":
            if len(i) != 13: print(f"{file}\n{len(i)}\n{i}")
            if re.match(inte, i[1]) == None and i[1] != "dnf": print(f"{file}\n{i}")
            if re.match(lapTime, i[2]) == None and i[2] != "unfinished": print(f"{file}\n{i}")
            if i[3] != "P" and i[3] != "did not pit" and i[3] != "pit": print(f"{file}\n{i}")
            for j in i[4:-1]:
                if re.match(lapTime, j) == None and re.match(secTime, j) == None and j != "no section time":
                    print("")
                    print(j)
                    print(f"{file}\n{i}")
            if re.match(avgSpeed, i[-1]) == None and i[-1] != "missing speed": print(f"{file}\n{i}")

            assert len(i) == 13
            assert re.match(inte, i[1]) or i[1] == "dnf"
            assert re.match(lapTime, i[2]) or i[2] == "unfinished"
            assert i[3] == "P" or i[3] == "did not pit" or i[3] == "pit"
            for j in i[4:-1]:
                assert re.match(lapTime, j) or re.match(secTime, j) or j == "no section time"
            assert re.match(avgSpeed, i[-1]) or i[-1] == "missing speed"


########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

#
# def addLists(file, nats, manus, riders, teams):
#     whole, date = openPDF(file)
#     for i in whole:
#         if 115.319 < i["x0"] < 115.321:
#             print("###############################################################################################################################################################################################################################################################################################")
#             print(i["text"])
#

#

#

#

#

#



#

#

#



# def getGLap(lis):
#     row = []
#     name = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")
#     lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
#     secTime = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}$")
#     avgSpeed = re.compile("^\d{2,3}[.]\d$")
#
#     row.append(lis[0])
#     del lis[0]
#     row.append(lis[0])
#     del lis[0]
#     if lis[0] != "P":
#         row.append("did not pit")
#     while True:
#         if len(lis) == 0:
#             break
#         if re.match(name, lis[0]):
#             break
#         elif re.match(avgSpeed, lis[0]):
#             row.append(lis[0])
#             del lis[0]
#             break
#         elif len(lis) > 2:
#             if re.match(lapTime, lis[2]):
#                 row.append(lis[0])
#                 del lis[0]
#                 break
#         row.append(lis[0])
#         del lis[0]
#
#     lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#     for i in lapLength:
#         if len(row) < i:
#             row.insert(-1, f"noTime")
#
#     row.insert(0, "lap")
#     return row
#
# def getBLap(lis):
#     row = []
#     lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
#     avgSpeed = re.compile("^\d{2,3}[.]\d$")
#
#     row.append("dnf")
#     row.append(lis[0])
#     del lis[0]
#     if lis[0] != "P":
#         row.append("did not pit")
#     while True:
#         if len(lis) == 0:
#             break
#         if re.match(avgSpeed, lis[0]):
#             row.append(lis[0])
#             del lis[0]
#             break
#         else:
#             row.append(lis[0])
#             del lis[0]
#
#     lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
#     for i in lapLength:
#         if len(row) < i:
#             row.insert(-1, f"noTime")
#
#     row.insert(0, "lap")
#     return row
#

#

#

#
# def badSave(file):
#     # """depricated???"""
#
#     badFiles = []
#     dest = "C:/Users/LuciusFish/Desktop/csv/mistakenFiles.csv"
#
#     with open(dest) as saveFile:
#         contents = saveFile.readlines()
#         for line in contents:
#             x = line
#             badFiles.append(x)
#
#     del badFiles[0]
#
#     badFiles.append(file)
#     saveCSV(badFiles, dest)
#
# def goodSave(file):
#     # """depricated???"""
#     finFiles = []
#     dest = "C:/Users/LuciusFish/Desktop/csv/finishedFiles.csv"
#
#     with open(dest) as saveFile:
#         contents = saveFile.readlines()
#         for line in contents:
#             x = line
#             finFiles.append(x)
#     finFiles.append(file)
#
#     del finFiles[0]
#
#     saveCSV(finFiles, dest)
#
# def intSaveFiles():
#     # """depricated???"""
#     try:
#         finFiles = []
#         badFiles = []
#
#         with open(save) as saveFile:
#             contents = saveFile.readlines()
#             for line in contents:
#                 x = line[:-1]
#                 finFiles.append(x)
#
#         with open(dest) as bFile:
#             contents = bFile.readlines()
#             for line in contents:
#                 x = line
#                 badFiles.append(x)
#         good = "C:/Users/LuciusFish/Desktop/csv/finishedFiles.csv"
#         bad = "C:/Users/LuciusFish/Desktop/csv/mistakenFiles.csv"
#
#         saveCSV(finFiles, good)
#         saveCSV(badFiles, bad)
#
#     except:
#         finFiles = []
#         badFiles = []
#         good = "C:/Users/LuciusFish/Desktop/csv/finishedFiles.csv"
#         bad = "C:/Users/LuciusFish/Desktop/csv/mistakenFiles.csv"
#         saveCSV(finFiles, good)
#         saveCSV(badFiles, bad)
#
#     return finFiles
#

#

#
# def getStats(lis):
#     # """Double checks that the following data represents a rider and there
#     # hasn't been a mix-up.  Spaghetti code, I know."""
#
#     low = []
#     longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
#     lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
#     avgSpeed = re.compile("^\d\d\d[.]\d$")
#     slowSpeed = re.compile("^\d\d[.]\d$")
#
#     low.append("Tyre")
#     while True:
#         if len(lis) == 0:
#             break
#         if re.match(lapTime, lis[1]["text"]) or \
#                 lis[0]["text"] == "PIT" or \
#                 lis[0]["text"] == "unfinished" or \
#                 re.match(longLap, lis[1]["text"]):
#             break
#         low.append(lis[0])
#         del lis[0]
#     row = getRiderRow(low)
#
#     return row