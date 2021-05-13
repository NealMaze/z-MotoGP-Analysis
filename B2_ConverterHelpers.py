# imports
from os import listdir, mkdir
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import os
import sys
from GenGetters import *
from time import sleep
from winsound import Beep

def getAnalyFiles(yr, dir, string):
    # """Searches the directory for appropriate files and creates a list to cycle through"""

    filter_files = fnmatch.filter(listdir(dir), f"{string}.pdf")
    files = [f"{dir}/{file}" for file in filter_files]

    return files

def addLists(file, nats, manus, riders, teams):
    whole, date = openPDF(file)
    for i in whole:
        if 115.319 < i["x0"] < 115.321:
            print(i["text"])

def openPDF(rcFile):
    # """Opens the PDF as a list and returns the list and the date of the event"""

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
    const = date
    for i in u[:4]:
        const.insert(0, i)

    return const

def parsePDF(col):
    # """Turns the PDF list into  a list of rows, and each row, either a lap, or rider or a new run"""

    rows = []
    counter = 0

    while len(col) != 0:
        catch = len(col)
        for i in col[:10]:
            print(i)

        row = runRow(col)






        if len(col) == catch:
            counter += 1
            if counter == 5:
                print("")
                print("looping")
                for row in rows[-5:]:
                    print(row)
                sys.exit()


    # while len(col) != 0:
    #     ty = len(col)
    #     row = runRow(col, const, file)
    #     r = []
    #     for i in row:
    #         r.append(i[text])
    #     if r != []:
    #         rows.append(r)


    return rows

def runRow(lis, const, file):
    # """Takes either the first item or second item out of the list,
    # determines what kind of data the following represents, removes it
    # from the list and returns that data.  Only returns one row at a time"""
    row = []

    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d$")
    avgSpeed = re.compile("^\d\d\d[.]\d$")
    slowSpeed = re.compile("^\d\d[.]\d$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")

    print(lis[0])
    if len(lis) == 0:
        row = []

    elif lis[0]["text"] == "unfinished" or lis[0]["text"] == "PIT":
        row = getBLap(lis)

    elif re.match(lapTime, lis[1]["text"]):
        row = getGLap(lis)

    # elif:
    #     low = []
    #     while re.match(lapTime, lis[1]["text"]) != True:
    #         low.append(lis[0])
    #         del lis[0]
    #     row = getRiderRow(low)
    #     rowAddConst(row, const)

    return row

#

#

#

#

#

#

#

#
# def getRiderRow(row):
#     r = []
#     print("")
#     for i in row:
#         print(i)
#         r.append(i)
#
#     rider = ["-pos-", "-number-", "-f_name-", "-l_name-", "-manufacturer-", "-nation-",
#              "-team-", "-t_laps-", "-runs-", "-f_Tyre-", "-r_Tyre-",
#              "-f_Age-", "-r_Age-", "-extra-"]
#
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#
#     while len(r) !=0:
#         i = r[0]
#         if re.match(position, i):
#             rider[0] = i
#         # elif i[""]
#
#
#
#
#
#     # if r[-1] == "Tyre":
#     #     rider[11] = r[-2]
#     #     del r[-2:]
#     #     if r[-1] == "Tyre":
#     #         rider[10] = r[-2]
#     #         del r[-2:]
#     #
#     # x = 0
#     # trash = ["MotoGP", "Tyre", "Moto2", "Moto3"]
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#     # nats = getListFils
#     # manufacturers = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA"]
#     #
#     # while x < len(r):
#     #     if tooMany == 500:
#     #         print("too many in getRider(1)")
#     #     tooMany += 1
#     #     if r[x] in trash:
#     #         del r[x]
#     #     elif re.match(position, r[x]):
#     #         del r[x]
#     #     elif r[x] == "Total":
#     #         strLaps = r[x+1]
#     #         laps = strLaps.replace("laps=", "")
#     #         rider[6] = laps
#     #         del r[x:x+3]
#     #     elif r[x] in nations:
#     #         rider[4] = r[x]
#     #         del r[x]
#     #     elif r[x] == "Run":
#     #         rider[7] = r[x+2]
#     #         del r[x:x+3]
#     #     elif r[x] in manufacturers:
#     #         rider[3] = r[x]
#     #         del r[x]
#     #     else:
#     #         x += 1
#     #
#     # x = 0
#     # while x < len(r):
#     #     if tooMany == 500:
#     #         print("too many in getRider(2)")
#     #     tooMany += 1
#     #     if re.match("^\d{1,2}$", r[x]):
#     #         rider[0] = r[x]
#     #         del r[x]
#     #     elif r[x] == "Front":
#     #         rider[8] = r[x+1]
#     #         del r[x:x+2]
#     #     elif r[x] == "Rear":
#     #         rider[9] = r[x+1]
#     #         del r[x:x+2]
#     #     else:
#     #         x += 1
#     #
#     # str = ""
#     # for i in r:
#     #     str += f" {i}"
#     #
#     # rider[-1] = str
#     print(rider)
#     return rider
#
# def rowAddConst(row, const):
#     # """Adds the event data to the row"""
#     for i in const:
#         row.insert(0, i)
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
#     # """accepts a matrix, and a file destination, and saves
#     # the matrix as a csv file"""
#
#     df = pd.DataFrame(mat)
#     df.to_csv(file, index=False)
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