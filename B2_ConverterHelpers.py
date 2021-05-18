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
    else:
        for i in finFiles:
            print(i)
    print("\n")

    return finFiles

def getAnalyFiles(dir, string):
    filterFiles = fnmatch.filter(listdir(dir), f"{string}")
    files = [f"{dir}/{file}" for file in filterFiles]

    return files

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
    # """Strips the boiler plate off the PDF list"""

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
            L.append(i)
        elif iVal > 309:
            R.append(i)

    for i in R:
        L.append(i)

    return L

def getConst(yr, file, date):
    # """Gets the event data"""
    r = file.replace(f"{yr}-", "")
    o = r.replace(".csv", "")
    u = o.split("-")
    x = u[-1]
    y = x.split("_")
    j = u[0]
    k = j.replace("/", "")
    track = u[3]
    trk = track.strip()
    const = []

    const.insert(0, date[1])
    const.insert(0, date[0])
    const.insert(0, u[1])
    const.insert(0, k)
    const.insert(0, trk)
    const.insert(0, y[0])

    return const

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

def parsePDF(col, const):
    # """Turns the PDF list into a list of rows, and each row, either a lap, or rider or a new run"""

    rows = []
    counter = 0

    while len(col) != 0:
        catch = len(col)
        row = runRow(col, const)
        print("\n#############################################################################\n")
        print("add names, team, and tire ages")
        print("\n#############################################################################\n")
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

def runRow(lis, const):
    # """Takes either the first item or second item out of the list,
    # determines what kind of data the following represents, removes it
    # from the list and returns that data.  Only returns one row at a time"""

    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    slowSpeed = re.compile("^\d\d[.]\d$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    name = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")

    if len(lis) < 1:
        row = []

    elif len(lis) < 2:
        print("line 180, helpers #####################################################################################################################################################################")
        print(lis)
        exit()

    elif lis[0]["text"] == "unfinished" or lis[0]["text"] == "PIT":
        print("bad lap")
        row = getBLap(lis)

    elif re.match(lapTime, lis[1]["text"]):
        print("good lap")
        row = getGLap(lis)

    elif re.match(position, lis[0]["text"]) or re.match(name, lis[0]["text"]):
        print("rider")
        yr = const[-1]
        low = []
        while True:
            low.append(lis[0])
            del lis[0]
            if len(lis) < 1:
                break
            if re.match(lapTime, lis[1]["text"]):
                break
        row = getRiderRow(low, yr)
        rowAddConst(row, const)

    else:
        print("")
        print(f" - - - {yr}, {lge}, {sesType} - - - ")
        print("Line 196 Helpers ###########################################################################################################################################")
        for i in line[:4]:
            txt = i["text"]
            loq = i["x0"]
            print(f"{txt}       {loq}")
        print("##################################################################")

    # print(f"And now this:\n{row}\n")
    lmn = 0
    for i in row:
        print(f"line 228, index: {lmn},   {i}")
        lmn += 1
    return row

def getRiderRow(row, yr):
    rider = ["-0-number-", "-1-f_name-", "-2-l_name-", "-3-manufacturer-", "-4-nation-",
             "-5-team-", "-6-t_laps-", "-7-runs-", "-8-f_Tire-", "-9-r_Tire-",
             "-10-f_Age-", "-11-r_Age-", "-12-extra-"]
    trash = ["MotoGP", "Tyre", "Moto2", "Moto3"]
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")

    x = 0
    while x < len(row):
        val = row[x]["text"]
        if val in trash:
            del row[x]
        elif re.match(position, val):
            del row[x]
        elif val == "Total":
            strLaps = row[x+1]["text"]
            laps = strLaps.replace("laps=", "")
            rider[6] = laps
            del row[x:x+3]
        elif val in nats:
            rider[4] = val
            del row[x]
        elif val == "Run":
            rider[7] = row[x+2]["text"]
            del row[x:x+3]
        elif val in manus:
            rider[3] = val
            del row[x]
        else:
            x += 1

    x = 0
    while x < len(row):
        val = row[x]["text"]
        if re.match("^\d{1,2}$", val) and rider[0] == "-0-number-":
            rider[0] = val
            del row[x]
        elif val == "Front":
            rider[8] = row[x+1]["text"]
            del row[x:x+2]
        elif val == "Rear":
            rider[9] = row[x+1]["text"]
            del row[x:x+2]
        else:
            x += 1

    x = 0
    while x < len(rider):
        val = rider[x]
        if "Tyre" in val:
            rider[x] = val.replace("Tyre", "")
        else:
            x += 1

    string = ""
    for i in row:
        val = i["text"]
        string += f" {val}"

    rider[-1] = string.strip()

    return rider





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
#
def rowAddConst(row, const):
    yr = const[-1]
    for i in const:
        row.insert(0, i)

    rData = getRidersData(yr)

    for i in rData:
        m = i[6]
        manu = m.upper()
        if i[1] == row[2] and i[2] == row[6] and i[4] == row[10] and manu == row[9]:
            print(f"Applicable rData: {i}")
            name = i[3]
            team = i[5]
            x = name.split(" ", 1)
            row[7] = x[0]
            row[8] = x[1]
            row[11] = team

#

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


# def getMatrix(rows, yr):
#     # """Takes the list and removes the rider rows, and appends all the lap
#     # rows with the appropriate rider data"""
#
#     matrix = []
#     rider = ["none"]
#
#     for row in rows:
#         if row[0] == yr:
#             rider = row
#         else:
#             lap = []
#             for i in rider[:-1]:
#                 lap.append(i)
#             for i in row:
#                 lap.append(i)
#             lap.append(rider[-1])
#             matrix.append(lap)
#
#     return matrix
#
# def saveCSV(mat, file):
#     df = pd.DataFrame(mat)
#     df.to_csv(file, index=False)
#
# def getGLap(lis):
#     # """After determinging that the following data represents a good lap, it
#     # takes the applicable dat off that list, formats it as a lap and returns it."""
#     row = []
#     longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
#     lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
#     avgSpeed = re.compile("^\d\d\d[.]\d$")
#     slowSpeed = re.compile("^\d\d[.]\d$")
#
#     row.append(lis[0])
#     del lis[0]
#     row.append(lis[0])
#     del lis[0]
#     while True:
#         if len(lis) == 0:
#             break
#         if re.match(avgSpeed, lis[0]) or \
#             re.match(slowSpeed, lis[0]):
#             row.append(lis[0])
#             del lis[0]
#             break
#         if len(lis) > 2:
#             if re.match(lapTime, lis[2]) or \
#                 re.match(longLap, lis[2]):
#                 row.append(lis[0])
#                 del lis[0]
#                 break
#         row.append(lis[0])
#         del lis[0]
#
#     lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#     for i in lapLength:
#         if len(row) < i:
#             row.insert(-1, f"Tsec{i - 3}")
#
#     return row
#
# def getBLap(lis):
#     # """After determing that the following data represents an unfinished lap, this
#     # removes the applicable data, and formats it as a lap to return"""
#
#     row = []
#     longLap = re.compile("^\d\d[']\d\d[.]\d\d\d$")
#     lapTime = re.compile("^\d[']\d\d[.]\d\d\d$")
#     avgSpeed = re.compile("^\d\d\d[.]\d$")
#     slowSpeed = re.compile("^\d\d[.]\d$")
#
#     row.append("dnf")
#     while True:
#         if len(lis) == 0:
#             break
#         if re.match(avgSpeed, lis[0]) or \
#             re.match(slowSpeed, lis[0]):
#             row.append(lis[0])
#             del lis[0]
#             break
#         else:
#             row.append(lis[0])
#             del lis[0]
#
#     lapLength = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
#     for i in lapLength:
#         if len(row) < i:
#             row.insert(-1, f"Tsec{i - 3}")
#
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