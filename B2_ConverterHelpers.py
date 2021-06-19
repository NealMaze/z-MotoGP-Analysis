# imports
from os import listdir, mkdir
from datetime import datetime
import pdfplumber as plumb
import fnmatch
import pandas as pd
import re
import os
import csv
import sys
from time import sleep
from winsound import Beep
from lists import *

def getFiles(dir, string):
    # gets Files from the provided dir matching the provided string
    filterFiles = fnmatch.filter(listdir(dir), f"{string}")
    files = [f"{dir}{file}" for file in filterFiles]
    return files

def getSaveName(file, sesType):
    # calculates a new file name, round, and track name for the csv file
    y = file.replace(pdfDir, "")
    t = y.split("-")
    round = t[1]
    lge = t[2]
    track = t[4].strip()
    fTrack = track.replace(" Marco Simoncelli", "")
    yr = t[0].replace("/", "")
    saveName = f"{yr}-{lge}-{round}-{fTrack}-{sesType}-Analysis.csv"
    z = csvSesDir + saveName

    return z, fTrack, round

def openPDF(rcFile):
    # opens the pdf as a list of dictionaries and also returns the date for the session
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
    # Gets the date of the event and returns it to the openPDF() function
    month = None
    words = pages[0].extract_words()
    date = []

    count = 0
    for i in words:
        x = i["text"].replace(",", "").lower()
        if x in months:
            month = x.capitalize()
            day = words[count+1]["text"]
            day = day.replace(",", "")
            day = day.lstrip("0")
            break

        x = i["text"].replace(",", "")
        if x in months:
            month = x.capitalize()
            day = words[count + 1]["text"]
            day = day.replace(",", "")
            day = day.lstrip("0")
            break

        count += 1

    if month == None:
        print(month)
        print(day)
        exit()

    date.append(month)
    date.append(day)

    return date

def stripBoilerPlate(lis):
    # removes any dictionaries that represent the header and footer of each page of the pdf
    # then it separates the remaining dictionaries into the left and right columns and then
    # appends the right side to the left side
    L = []
    R = []
    nonGrata = ["T4", "T4Speed"]

    x = 0
    for i in lis:
        if i["text"] in nonGrata:
            x += 1
            y = x
        else:
            x += 1
    del lis[:y]

    if lis[0]["text"] == "Speed":
        del lis[0]

    x = 0
    while "Fastest" not in lis[x]["text"]:
        x += 1
        if lis[x]["text"] == "These":
            break
        if lis[x]["text"] == "FIM" and lis[x+1]["text"] == "ROAD":
            break
        if lis[x]["text"] == "MotoGP" and lis[x+1]["text"] == "MotoGP":
            break
        if lis[x]["text"] == "DORNA" and lis[x+1]["text"] == "MotoGP":
            break
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

def parsePDF(col):
    # cycles through the pdf dictionaries, and turns it into a list of lists representing riders, runs, and laps.
    # also deletes bad data returns
    rows = []
    counter = 0

    while len(col) != 0:

        catch = len(col)
        row = getRow(col)
        if row != []:
            rows.append(row)

        if len(col) == catch:
            counter += 1
            if counter == 5:
                print("")
                print("looping")
                for row in rows[-5:]:
                    print(row)
                exit("\nline 156")

    return rows

def getRow(lis):
    # examins the first couple items of the list and, passes the list to the appropriate row parser
    # then deletes the parsed row from the list and returns the row to the parsePdf() function
    if len(lis) < 1: exit("\nempty row\nline 179")
    elif len(lis) < 2: exit("line 177, helpers\nline 177")
    elif lis[0]["text"] == "unfinished" or lis[0]["text"] == "PIT": row = getLap(lis)

    elif lis[1]["text"] == "unfinished" or lis[1]["text"] == "PIT" or re.match(secTime, lis[1]["text"]):
        row = getLap(lis)

    elif re.match(lapTime, lis[1]["text"]) or re.match(pitTime, lis[1]["text"]) or \
            re.match(pitTime, str(lis[0]["text"])): row = getLap(lis)

    elif lis[0]["text"] == "Run" or lis[0]["text"] == "Run#" or lis[0]["text"] == "run" or lis[0]["text"] == "run#":
        row = getRun(lis)

    elif re.match(position, lis[0]["text"]) or re.match(name, lis[0]["text"]) or re.match(name, lis[1]["text"]):
        row = getRiderRow(lis)
        # print(row)

    else:
        row = getLap(lis)
        row[0] = "bad"

    if row[0] != "bad":
        row = delBadTimes(row)

    return row

def getRiderRow(lis):
    # parses a rider row and returns it to the getRow() function
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    runs = ["Run", "run", "Run#", "run#", "unfinished", "PIT"]
    row = ["rider"]
    while True:
        if len(lis) < 2:
            row.append(lis[0]["text"])
            del lis[0]
            break
        elif lis[0]["text"] in runs or re.match(lapTime, lis[1]["text"]): break
        elif "laps=" in row[-1] and "laps=" in row[-2]: break
        else:
            row.append(lis[0]["text"])
            del lis[0]

    return row

def delBadTimes(items):
    # deletes bad lap times or bad section times and also marks bad rider rows for deletion
    x = []
    count = 0

    for i in items:
        if re.match(bSecTime, i) or re.match(bLapTime, i):
            x.insert(0, count)
        count += 1

    if len(x) != 0:
        if items[0] == "rider":
            items[0] = "bad"
        for i in x:
            del items[int(i)]

    return items

def getRun(lis):
    # parses a run row and returns it to the getRow() function
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d$")
    row = []
    while True:
        row.append(lis[0]["text"])
        del lis[0]
        if len(lis) < 2:
            row.append(lis[0]["text"])
            del lis[0]
            break
        elif re.match(lapTime, lis[1]["text"]) or re.match(secTime, lis[1]["text"]):
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

def getLap(lis):
    # parses a lap row and returns it to the getRow() function
    mashUp = False
    nSplit = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}[*]\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    oSplit = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}[*]\d{1,2}[.]\d{3}[*]{0,1}$")
    pSplit = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}[*]\d{1,2}[.]\d{3}[*]{0,1}$")
    qSplit = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}[*]\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    headerPass = ["unfinished", "P", "b", "PIT"]
    loq = lis[0]["top"]
    hi = loq + 1
    lo = loq - 1
    row = []
    header = []
    footer = []
    cRow = ["lap"]
    fRow = ["sect", "missing", "missing", "missing", "missing"]
    sections = []

    while True:
        if len(lis) == 0:
            break
        elif lis[0]["top"] > hi:
            break
        elif lis[0]["top"] < lo:
            break
        else:
            row.append(lis[0])
            del lis[0]

    for i in row:
        iLoq = int(i["x0"])
        txt = str(i["text"])
        if txt in headerPass:
            header.append(txt)
        elif iLoq < 116 or int(i["x0"]) in range(305, 379):
            header.append(i["text"])
        elif int(i["x0"]) in range(117, 269) or int(i["x0"]) in range(380, 530):
            sections.append(i)
        elif int(i["x0"]) in range(270, 388) or int(i["x0"]) > 530:
            footer.append(i["text"])
        else: exit("\nline 310")

########################################################################################################################

    if len(sections) == 4:
        fRow[1] = sections[0]["text"]
        fRow[2] = sections[1]["text"]
        fRow[3] = sections[2]["text"]
        fRow[4] = sections[3]["text"]

    elif len(sections) > 4:
        print(sections)
        printer(sections)
        exit("\nline 328")

    else:
        nwRow = []
        for i in sections:
            if re.match(nSplit, i["text"]) or re.match(oSplit, i["text"]) \
                    or re.match(pSplit, i["text"]) or re.match(qSplit, i["text"]):
                mashUp = True
                txt = i["text"]
                j = i["text"].split("*", 1)
                k = j[0]
                l = k + "*"
                m = j[1]
                nwRow.append(l)
                nwRow.append(m)

            elif re.match(lapTime, i["text"]) or re.match(secTime, i["text"]) or re.match(pitTime, i["text"]):
                nwRow.append(i["text"])

        if mashUp == True and len(nwRow) == 4:
            fRow[1] = nwRow[0]
            fRow[2] = nwRow[1]
            fRow[3] = nwRow[2]
            fRow[4] = nwRow[3]

        else:
            # print("")
            for i in sections:
                t = str(i["text"])
                iLoq = int(i["x0"])
                # print(f"{t}     {iLoq}")
                if re.match(lapTime, t) or re.match(secTime, t) or re.match(pitTime, t):
                    if iLoq in range(117, 153) or iLoq in range(380, 415):
                        fRow[1] = t
                    elif iLoq in range(154, 193) or iLoq in range(416, 453):
                        fRow[2] = t
                    elif iLoq in range(194, 229) or iLoq in range(454, 491):
                        fRow[3] = t
                    elif iLoq in range(230, 269) or iLoq in range(492, 530):
                        fRow[4] = t
                    else:
                        print("")
                        print(f"{t}     {iLoq}")
                        exit("\nline 371")

########################################################################################################################

    if len(fRow) != 5:
        print("")
        for i in row:
            print(i)
        print("")
        print(fRow)
        exit("\nline 381")

    for i in header: cRow.append(i)
    for i in fRow: cRow.append(i)
    for i in footer: cRow.append(i)

    return cRow

def chkConst(const, yr):
    # checks that the date values in the Const variable match
    lMonth = const[1]
    day = const[2]

    if day not in days:
        print(f"\n\nline 428\n{const}\nday = {const[2]}")
        exit()
    if const[3] != yr:
        print(f"\n\nline 431\n{const}\nyear = {const[3]}\nexpected yr = {yr}")
        exit()

def getCRows(rows, yr, lge):
    # cleans the rows
    cRows = []
    for xRow in rows:
        row = []
        for i in xRow:
            row.append(i.lstrip("*"))

        if len(cRows) != 0 and row[1] == cRows[-1][1] and row[2] == cRows[-1][2]:
            del cRows[-1]
            lapNum -= 1

        row[0] = row[0].lower()

        if row[0] == "rider":
            lapNum = 1
            mRdr = matchRider(row, yr, lge)
            cRider = getCRider(row, mRdr)
            cRows.append(cRider)
            if len(cRider) < 9 or len(cRider) > 9:
                print("")
                print(cRider)
                exit("\nline 413")

        elif row[0] == "run":
            cRun = cleanRun(row)
            cRows.append(cRun)
            if len(cRun) < 6 or len(cRun) > 6:
                print("")
                print(cRun)
                exit("\nline 421")

        if row[0] == "lap":
            nuRow = row
            cLap = []

            cLap.append(nuRow[0])
            del nuRow[0]

########################################################################################################################
            # manage lapNum

            if len(nuRow) > 0:
                x = nuRow[0].lstrip("0")
                nuRow[0] = x

            if len(nuRow) < 1:
                cLap.append("missing")

            elif re.match(pitTime, nuRow[0]):
                cLap.append(nuRow[0][0])

            elif nuRow[0] == "unfinished":
                cLap.append("0")

            elif nuRow[0] == "cancelled":
                cLap.append("0")
                nuRow[0] = "unfinished"

            elif nuRow[0] == "sect":
                cLap.append("0")
                nuRow.insert(0, "unfinished")

            elif nuRow[0] == "PIT":
                cLap.append(lapNum)

            elif int(nuRow[0]) > -1:
                cLap.append(nuRow[0])
                del nuRow[0]

            elif re.match(pitTime, nuRow[0]):
                cLap.append(nuRow[0][0])

            elif nuRow[0] == "-1":
                cLap.append("0")
                del nuRow[0]

            else:
                print("\n")
                print(f"{nuRow[0]}")
                print(nuRow)
                exit("\nline 461")

########################################################################################################################
            # manage lapTime

            if len(nuRow) < 1:
                cLap.append("missing")

            elif re.match(lapTime, nuRow[0]) or re.match(secTime, nuRow[0]) or re.match(pitTime, nuRow[0]) or \
                    nuRow[0] == "PIT" or nuRow[0] == "unfinished":
                cLap.append(nuRow[0])
                del nuRow[0]

            else:
                print(f"line 114 - {nuRow[0]}")
                print(lapNum)
                print(nuRow)
                print(cLap)
                exit("\nline 508")

########################################################################################################################
            # manage pit booleon

            if len(nuRow) < 1:
                cLap.append("missing")

            elif cLap[-1] == "PIT" and nuRow[0] == "sect":
                cLap.append("P")

            elif nuRow[0] == "P" or nuRow[0] == "b":
                cLap.append("P")
                del nuRow[0]

            elif nuRow[1][0] == "P":
                nuRow[1] = nuRow[1].lstrip("P")
                cLap.append("P")

            elif nuRow[0] == "sect":
                cLap.append("did not pit")

            elif re.match(secTime, nuRow[0]) or re.match(lapTime, nuRow[0]) or re.match(avgSpeed, nuRow[0]):
                cLap.append("did not pit")
                exit(f"\n{cLap}\n{nuRow}\nline 538")

            else:
                print(f"line 461 - {nuRow[0]}")
                print(nuRow)
                print(cLap)
                exit("\nline 544")

########################################################################################################################
            # grab sect marker

            if nuRow[0] == "sect":
                cLap.append(nuRow[0])
                del nuRow[0]

            else: exit("\nline 553")

########################################################################################################################
            # manage section times

            while True:
                if len(cLap) == 9:
                    break

                if len(nuRow) < 1:
                    cLap.append("missing")

                elif re.match(avgSpeed, nuRow[0]):
                    cLap.append("missing")

                elif re.match(secTime, nuRow[0]) or re.match(lapTime, nuRow[0]) or re.match(pitTime, nuRow[0]):
                    cLap.append(nuRow[0])
                    del nuRow[0]

                elif nuRow[0] == "missing":
                    cLap.append(nuRow[0])
                    del nuRow[0]

                else:
                    print(f"line 591 - {nuRow[0]}")
                    print(nuRow)
                    exit("\nline 579")


########################################################################################################################
            # manage avgSpeed

            if len(nuRow) < 1 and len(cLap) < 14:
                cLap.append("missing")

            elif re.match(avgSpeed, nuRow[0]):
                cLap.append(nuRow[0])
                del nuRow[0]

            else:
                print(f"line 191 - {nuRow[0]}")
                print(nuRow)
                exit("\nline 595")

            if len(cLap) > 14: exit("\nline 599")

            if len(nuRow) > 0: exit("\nline 603")

########################################################################################################################
            if cLap[2] == "PIT" and cLap[3] != "P": exit(f"\nline 620\nproblem\n{cLap}\n")
            cRows.append(cLap)
            lapNum += 1

    return cRows

def matchRider(row, yr, lge):
    # matches rider to rider in rider csv file
    yrRiders = getRidersData(yr)
    bMatches = []
    bRdr = []

    rStr = ""
    for i in row[1:]:
        if "laps=" in i: pass
        else: rStr = rStr + " " + i

    for rdr in yrRiders:
        if rdr[1] == lge:
            matches = []
            manu = rdr[6]
            uManu = manu.upper()
            name = rdr[3].split(" ")
            fName = name[0]
            lName = name[1]
            if len(lName) > 5:
                lName = lName[:5]

            if rdr[2] in rStr: matches.append("num")
            if fName in rStr: matches.append("fName")
            if lName in rStr: matches.append("lName")
            if rdr[4] in rStr: matches.append("nat")
            if rdr[5] in rStr: matches.append("team")
            if uManu in rStr: matches.append("manu")
            if lName in rdr[3]: matches.append("lName")

            if len(matches) < 3: pass
            elif len(matches) > len(bMatches):
                bMatches = matches
                bRdr = rdr
                b_fName = fName
                b_lName = lName
                b_Num = rdr[2]

    if "fName" and "lName" not in bMatches:
        rCnt = 0
        cnt = 0
        tstName = ""

        try:
            while True:
                if tstName == bRdr[3]:
                    break
                sl = rStr[cnt]
                rnl = bRdr[3][rCnt]
                if sl == rnl:
                    tstName = tstName + rnl
                    rCnt += 1
                    cnt += 1
                else:
                    cnt += 1

        except:
            print("\n")
            print(row)
            print(f"best matches = {bMatches}")
            print(f"fName = {b_fName}")
            print(f"lName = {b_lName}")
            print(f"b_Num = {b_Num}")
            print(f"")
            print(row[3])
            print("")
            print(f"row = {row}")
            print(f"bRdr  = {bRdr}")
            exit("\nline 681")

    return bRdr

def getRidersData(yr):
    # opens the rider csv file and returns contents to the matchRider() function
    data = []
    rows = []

    with open(f"{csvRidersDir}{yr}RidersV2.csv", "r", encoding="utf8") as yrFile:
        i = csv.reader(yrFile, delimiter=",")
        for r in i:
            rows.append(r)

    if len(rows[0]) < 3:
        print("row too short")
        for i in rows[0]:
            print(i)
            data.append(i)
        exit("\nline 699")

    elif len(rows[0]) > 3:
        for row in rows:
            data.append(row)

    return data

def getCRider(row, mRdr):
    # returns a cleaned rider row
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    cRdr = ["0-pos", "1-num", "2-fName", "3-lName", "4-nat", "5-team", "6-manu", "missing"]

    if mRdr == []:
        print("wrong mRdr")
        print("getCRider() fail")
        exit("\nline 714")

    cRdr[1] = mRdr[2]
    name = mRdr[3].split()
    cRdr[2] = name[0]
    cRdr[3] = name[1]
    cRdr[4] = mRdr[4]
    cRdr[5] = mRdr[5]
    cRdr[6] = mRdr[6]

    m = 0
    while len(row) > m:
        if re.match(position, row[m]):
            cRdr[0] = row[m]
        elif row[m] == "Total":
            numLaps = row[m+1]
            cRdr[7] = numLaps.replace("laps=", "")
        m += 1

    cRdr.insert(0, "rider")
    return cRdr

def cleanRun(row):
    # returns a cleaned run row
    while len(row) < 6: row.append("missing")

    if row[1] == "-":
        row[1] = "missing"
    if row[2] == "-":
        row[2] = "missing"
    if row[3] == "-":
        row[3] = "missing"

    if row[2] not in tires:
        row[2] = "missing"
    if row[3] not in tires:
        row[3] = "missing"

    if re.match(inte, row[4]) == None \
            and re.match(inte, row[5]) == None \
            and row[4] != "missing" \
            and row[5] != "missing":
        print(row)
        print(
            "ages")
        exit("line 730")
    else:
        return row

def chkRider(row, yr):
    # checks a rider row and tests that the values are appropriate to their position
    rdrData = getRidersData(yr)
    nats = []
    manus = []
    for rdr in rdrData:
        if rdr[4] not in nats:
            nats.append(rdr[4])
        if rdr[6] not in manus:
            manus.append(rdr[6])

    if len(row) != 9:
        print("")
        print("B2_ConverterHelpers.py chkRider(row)")
        print("row wrong length")
        print(row)
        exit()

    if re.match(position, row[1]) == None and row[1] != "0-pos":
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 0")
        print(row[1])
        print(row)
        exit()

    if re.match(inte, row[2]) == None and int(yr) > 2006:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[2])
        print(row)
        exit()

    if re.match(name, row[3]) == None:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 2")
        print(row[3])
        print(row)
        exit()

    if re.match(name, row[4]) == None:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 3")
        print(row[4])
        print(row)
        exit()

    if row[5] not in nats:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 4")
        print(row[5])
        print(row)
        exit()

    if row[7] not in manus:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 5")
        print(row[7])
        print(row)
        exit()

    if re.match(inte, row[8]) == None and row[8] != "missing":
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 6")
        print(row[8])
        print(row)
        exit()

def chkRun(row):
    # checks a run row and verifies values
    if len(row) != 6:
        print("B2_ConverterHelpers.py chkRun(row) - 1")
        print("row wrong length")
        print(row)
        exit("\nline 874")

    if re.match(inte, row[1]) == None and row[1] != "missing":
        print("B2_ConverterHelpers.py chkRun(row) - 2")
        print("row[1]")
        print(row[1])
        print(row)


    if row[2] not in tires:
        print("B2_ConverterHelpers.py chkRun(row) - 2")
        print(row[2])
        print(row)
        exit()

    if row[3] not in tires:
        print("B2_ConverterHelpers.py chkRun(row) - 2")
        print(row[3])
        print(row)
        exit()

    if re.match(inte, row[4]) and row[4] == "missing":
        print("B2_ConverterHelpers.py chkRun(row) - 2")
        print(row[4])
        print(row)
        exit()

    if re.match(inte, row[5]) and row[5] == "missing":
        print("B2_ConverterHelpers.py chkRun(row) - 2")
        print(row[5])
        print(row)
        exit()

def chkLap(row, lapNum):
    # check the length of the lap row
    if len(row) != 10:
        exit(f"\n{len(row)}\n{row}\nline 814")

    # check that the lap number is sequential and that row[1] can be turned into an int
    intRow = int(row[1])
    lapNum = int(lapNum)
    if intRow != 0:
        lapNum += 1

    # check that row[2] is some type of lap time
    if re.match(lapTime, str(row[2])) == None and \
            re.match(secTime, str(row[2])) == None and \
            re.match(pitTime, str(row[2])) == None and \
            row[2] != "missing" and row[2] != "PIT" and\
            row[2] != "unfinished":
        print("")
        print("chkLap(row)")
        print("row[2]")
        print(row[2])
        print(row)
        exit("\nline 840")

    # check that row[3] represents a pit boolean
    if row[3] != "P" and row[3] != "did not pit" and row[3] != "missing":
        print("")
        print("chkLap(row)")
        print("row[3]")
        print(row[3])
        exit("\nline 847")

    # check that row[4] == "sect"
    if row[4] != "sect": exit(f"\n{row}\nline 849")

    # check that the following 8 positions represent section times
    for i in row[5:9]:
        if re.match(secTime, i) or re.match(lapTime, i) or re.match(pitTime, i) or i == "missing": pass
        else:
            exit(f"\nchkLap(row)\nline 917\n{i}\n{row[5:9]}")

    # check that the avgSpeed value matches formatting
    if re.match(avgSpeed, row[9]) == None and row[9] != "missing":
        exit(f"\nchkLap(row)\nline 921\n{row[9]}")

    if row[1] != "0": lapNum = row[1]
    return lapNum

def getMatrix(rows, const):
    # combines the const, and rows into one single type of row
    matrix = []
    if len(const) != 8:
        print(f"len(const) = {len(const)}")
        print(f"const = {const}")
        exit("\nline 912")
    irun = ["runNum", "fTire", "rTire", "0", "0"]

    for row in rows:
        xLap = []
        if row[0] == "rider":
            rider = row[1:]
            run = irun
        elif row[0] == "run":
            run = row[1:]
        elif row[0] == "lap":
            lap = row[1:]
            for i in const[1:]: xLap.append(i)
            for j in rider: xLap.append(j)
            for k in run: xLap.append(k)
            for l in lap:
                if l == "sect": pass
                else: xLap.append(l)
            if len(xLap) != 28:
                print("xLap length problem")
                print(len(xLap))
                print(xLap)
                exit("\nline 935")
            matrix.append(xLap)
        else:
            print("B2_ConverterHelpers.py line 415")
            exit("\nline 939")

    return matrix

def matFormat(mat, id):
    # replaces place holders with null values, and removes the "Round_" lead from round values
    fMat = []
    nulls = ["missing", "did not pit", "runNum", "runnum"]

    for row in mat:
        fRow = []
        for i in row:
            if i in nulls:
                fRow.append(None)
            elif i == row[9] or i == row[10]:
                x = i.lower()
                fRow.append(x)
            elif "Round_" in i:
                j = i.replace("Round_", "")
                fRow.append(j)
            else:fRow.append(i)
        fMat.append(fRow)

    lineNum = 1000
    gMat = []
    for row in fMat:
        gRow = row
        rID = id + str(lineNum)
        gRow.insert(0, rID)
        gMat.append(gRow)
        lineNum += 1

    return gMat

def saveCSV(mat, file, headers):
    # saves the matrix to a csv file using the headers as column headers
    df = pd.DataFrame(mat)
    df.to_csv(file, index=False, header = headers)
    print(file.replace(csvSesDir, ""))

def printer(lis):
    # takes the text value out of each dicionary in the argued list and prints them in a list
    printer = []
    for i in lis:
        printer.append(i["text"])
    print(printer)

def strToSec(strTime):
    timeAsString = strTime
    secList = [timeAsString, None, False]
    passables = [None, "PIT", "unfinished"]

    if strTime in passables: pass

    else:
        totalSec = 0
        subString = strTime

        if "*" in subString:
            subString = subString.replace("*", "")
            secList[2] = True

        if ":" in subString:
            hours, subString = subString.split(':')
            totalSec = int(hours) * 3600

        if "'" in subString:
            minutes, subString = subString.split("'")
            totalSec = int(minutes) * 60

        totalSec += float(subString)
        totSec = round(totalSec, 3)

        secList[1] = totSec

    return secList

def secToStr(totSec):
    # ended up not needing this but leaving it incase it becomes useful later
    hours = int(totSec) // 3600
    minutes = (int(totSec) % 3600) // 60
    seconds = totSec % 60

    if hours > 0:
        strTime = f"{hours}:{minutes:02}'{seconds}"
    elif minutes > 0:
        strTime = f"{minutes:02}'{seconds}"
    else: strTime = f"{seconds}"

    return strTime

def getSeconds(row):
    nuRow = []

    index = row[0].replace("Moto", "").replace("*", "")
    nuRow.append(index)

    for i in row[1:22]:
        nuRow.append(i)

    lapList = strToSec(row[22])
    for i in lapList: nuRow.append(i)

    if row[23] == "P": nuRow.append(True)
    else: nuRow.append(False)

    for i in row[24:-1]:
        secList = strToSec(i)
        for i in secList: nuRow.append(i)

    nuRow.append(row[-1])

    return nuRow

def processSeconds(matrix):
    nuMatrix = []

    for row in matrix:
        nuRow = getSeconds(row)
        nuMatrix.append(nuRow)

    return nuMatrix


