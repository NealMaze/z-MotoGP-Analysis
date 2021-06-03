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

def getSaveName(file, sesType):
    y = file.replace(pdfDir, "")
    t = y.split("-")
    round = t[1]
    lge = t[2]
    track = t[4].strip()
    fTrack = track.replace(" Marco Simoncelli", "")
    yr = t[0].replace("/", "")
    saveName = f"{yr}-{lge}-{round}-{fTrack}-{sesType}-Analysis.csv"
    z = csvDir + saveName
    return z, fTrack

def getAnalyFiles(dir, string):
    filterFiles = fnmatch.filter(listdir(dir), f"{string}")
    files = [f"{dir}{file}" for file in filterFiles]

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
                exit()

    return rows

def getRow(lis, yr):
    jokeLap = re.compile("^\d{1}[:]\d\d[']\d\d[.]\d\d\d[*]{0,1}$")
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    secTime = re.compile("^\d{1,2}[.]\d\d\d[*]{0,1}$")
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    name = re.compile("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")

    if len(lis) < 1:
        print("empty row")
        print("##########################################################################################################")
        row = []

    elif len(lis) < 2:
        print("line 177, helpers #####################################################################################################################################################################")
        print(lis[:10]["text"])
        print(f"B2_ConverterHelpers.py line 215")
        exit()

    elif lis[0]["text"] == "unfinished" or lis[0]["text"] == "PIT":
        val = "lap"
        row = getLap(lis)

    elif lis[1]["text"] == "unfinished" or lis[1]["text"] == "PIT" or re.match(secTime, lis[1]["text"]):
        val = "lap"
        row = getLap(lis)

    elif re.match(lapTime, lis[1]["text"]) or re.match(jokeLap, lis[1]["text"]):
        val = "lap"
        row = getLap(lis)

    elif lis[0]["text"] == "Run" or lis[0]["text"] == "Run#" or lis[0]["text"] == "run" or lis[0]["text"] == "run#":
        val = "run"
        row = getRun(lis)

    elif re.match(position, lis[0]["text"]) or re.match(name, lis[0]["text"]) or re.match(name, lis[1]["text"]):
        val = "rider"
        row = getRiderRow(lis)

    else:
        row = getLap(lis)
        row[0] = "bad"

    return row

def getRiderRow(lis):
    lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
    runs = ["Run", "run", "Run#", "run#", "unfinished", "PIT"]
    row = ["rider"]
    while True:
        if len(lis) < 2:
            row.append(lis[0]["text"])
            del lis[0]
            break
        elif lis[0]["text"] in runs or re.match(lapTime, lis[1]["text"]):
            break
        else:
            row.append(lis[0]["text"])
            del lis[0]

    return row

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

def getCRows(rows, yr, lge):
    cRows = []
    for row in rows:
        row[0] = row[0].lower()
        if row[0] == "rider":
            lapNum = 1
            mRdr = matchRider(row, yr, lge)
            cRider = getCRider(row, mRdr)
            cRows.append(cRider)
            if len(cRider) < 9 or len(cRider) > 9:
                print(cRider)
                exit()

        elif row[0] == "run":
            cRun = cleanRun(row)
            cRows.append(cRun)
            if len(cRun) < 6 or len(cRun) > 6:
                print(cRun)
                exit()

        if row[0] == "lap":
            template = ["lap", "lapNum", "lap time", "pit boolean", "sec time", "sec time", "sec time",
                        "sec time", "sec time", "sec time", "sec time", "sec time", "avg speed"]
            nuRow = row
            nuLap = []
            ########################################################################################################################
            # manage lap declaration and if lapNum doesn't match

            if len(nuRow) < 1:
                print("line 82")
                exit()

            if row[1] == "unfinished":
                lapNum -= 1

            elif re.match(inte, nuRow[1]) != None and nuRow[1] > str(lapNum):
                alNum = nuRow[1]
                print("\n")
                print(row)
                print("lap number in row higher than expected lap number")
                print(f"expected lap number = {lapNum}")
                print(f"actual lap number =   {alNum}")
                while True:
                    badLap = ["lap", lapNum, "missing", "missing", "missing", "missing", "missing", "missing",
                              "missing", "missing", "missing", "missing", "missing"]
                    cRows.append(badLap)
                    print(badLap)
                    lapNum += 1
                    if re.match(inte, nuRow[1]) != None and nuRow[1] == str(lapNum):
                        break

            elif nuRow[1] < str(lapNum) and re.match(inte, nuRow[1]) != None:
                alNum = nuRow[1]
                print("\n")
                print(row)
                print("lap number in row lower than expected lap number")
                print(f"expected lap number = {lapNum}")
                print(f"actual lap number =   {alNum}")
                exit()

            nuLap.append(nuRow[0])
            del nuRow[0]
            ########################################################################################################################
            # manage lapNum

            x = nuRow[0].lstrip("0")
            nuRow[0] = x

            if len(nuRow) < 1:
                nuLap.append("missing")

            elif re.match(inte, nuRow[0]):
                nuLap.append(nuRow[0])
                del nuRow[0]

            elif nuRow[0] == "PIT":
                nuLap.append(lapNum)

            elif nuRow[0] == "unfinished":
                nuLap.append("0")

            else:
                if nuRow[0] == "40.927":
                    nuRow = ["lap", lapNum, "missing", "missing", "missing", "missing", "missing", "missing",
                              "missing", "missing", "missing", "missing", "missing"]
                else:
                    print("\n")
                    print(f"line 96 - {nuRow[0]}")
                    print(nuRow)
                    exit()
            ########################################################################################################################
            # manage lapTime

            if len(nuRow) < 1:
                nuLap.append("missing")

            elif re.match(lapTime, nuRow[0]) or re.match(secTime, nuRow[0]) or nuRow[0] == "PIT" or nuRow[0] == "unfinished":
                nuLap.append(nuRow[0])
                del nuRow[0]

            else:
                print(f"line 114 - {nuRow[0]}")
                print(nuRow)
                exit()
            ########################################################################################################################
            # manage pit booleon

            if len(nuRow) < 1:
                nuLap.append("missing")

            elif nuRow[0] == "P":
                nuLap.append(nuRow[0])
                del nuRow[0]

            elif re.match(secTime, nuRow[0]) or re.match(lapTime, nuRow[0]) or re.match(avgSpeed, nuRow[0]):
                nuLap.append("did not pit")

            else:
                print(f"line 131 - {nuRow[0]}")
                print(nuRow)
                print(nuLap)
                exit()
            ########################################################################################################################
            # manage section times

            while True:
                nSplit = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}[*]\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
                oSplit = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}[*]\d{1,2}[.]\d{3}[*]{0,1}$")
                pSplit = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}[*]\d{1,2}[.]\d{3}[*]{0,1}$")
                qSplit = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}[*]\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
                if len(nuRow) < 1 and len(nuLap) < 12:
                    nuLap.append("missing")

                elif len(nuLap) == 12:
                    break

                elif re.match(secTime, nuRow[0]) or re.match(lapTime, nuRow[0]):
                    nuLap.append(nuRow[0])
                    del nuRow[0]

                elif re.match(nSplit, nuRow[0]) or re.match(oSplit, nuRow[0]) \
                        or re.match(pSplit, nuRow[0]) or re.match(qSplit, nuRow[0]):
                    i = nuRow[0]
                    print(i)
                    j = i.split("*", 1)
                    k = j[0]
                    l = k + "*"
                    m = j[1]
                    del nuRow[0]
                    nuLap.append(l)
                    nuLap.append(m)

                elif re.match(avgSpeed, nuRow[0]):
                    break

                else:
                    print(f"line 156 - {nuRow[0]}")
                    print(nuRow)
                    exit()
            ########################################################################################################################
            # add times for missing sections

            while True:
                if len(nuLap) == 12:
                    break
                elif len(nuLap) > 12:
                    print(f"line 179 - {nuRow[0]}")
                    print(nuRow)
                    exit()
                else:
                    nuLap.append("no sec time")
            ########################################################################################################################
            # manage avgSpeed

            if len(nuRow) < 1:
                nuLap.append("missing")

            elif re.match(avgSpeed, nuRow[0]):
                nuLap.append(nuRow[0])
                del nuRow[0]

            else:
                print(f"line 191 - {nuRow[0]}")
                print(nuRow)
                exit()

            if len(nuLap) > 13:
                print("line 223")
                exit()

            cRows.append(nuLap)
            lapNum += 1

    return cRows

def saveCSV(mat, file):
    df = pd.DataFrame(mat)
    df.to_csv(file, index=False)

def matchRider(row, yr, lge):
    yrRiders = getRidersData(yr)
    bMatches = []
    bRdr = []

    rStr = ""
    for i in row[1:]:
        if "laps=" in i:
            lps = True
        else:
            rStr = rStr + " " + i

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
            print(f"best matches = {bMatches}")
            print(f"fName = {b_fName}")
            print(f"lName = {b_lName}")
            print(f"b_Num = {b_Num}")
            print(f"")
            print(row[3])
            print("")
            print(f"row = {row}")
            print(f"bRdr  = {bRdr}")
            exit()

    return bRdr

def getRidersData(yr):
    data = []
    rows = []

    with open(f"{csvDir}{yr}RidersV2.csv", "r", encoding="utf8") as yrFile:
        i = csv.reader(yrFile, delimiter=",")
        for r in i:
            rows.append(r)

    if len(rows[0]) < 3:
        print("row too short")
        for i in rows[0]:
            print(i)
            data.append(i)
        exit()

    elif len(rows[0]) > 3:
        for row in rows:
            data.append(row)

    return data

def getCRider(row, mRdr):
    position = re.compile("^\d{1,2}(st|nd|rd|th)$")
    cRdr = ["0-pos", "1-num", "2-fName", "3-lName", "4-nat", "5-team", "6-manu", "missing"]

    if mRdr == []:
        print("wrong mRdr")
        print("getCRider() fail")
        exit()

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
    while len(row) < 6: row.append("missing")

    if row[2] == "-":
        row[2] = "missing"
    if row[3] == "-":
        row[3] = "missing"

    if row[2] not in tires \
            or row[3] not in tires:
        print(row)
        print(
            "tires #############################################################################################################################################################################################")
        exit()

    if re.match(inte, row[4]) == None \
            and re.match(inte, row[5]) == None \
            and row[4] != "missing" \
            and row[5] != "missing":
        print(row)
        print(
            "ages ########################################################################################################################################################################################################")
        exit()
    else:
        return row

def chkRider(row, yr):
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

    if re.match(position, row[1]) == None:
        print("")
        print("B2_ConverterHelpers.py chkRider(row)")
        print(row[1])
        print(row)
        exit()
    if re.match(inte, row[2]) == None:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[2])
        print(row)
        exit()
    if re.match(name, row[3]) == None:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[3])
        print(row)
        exit()
    if re.match(name, row[4]) == None and row[4] != "BOOTH-AMOS":
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[4])
        print(row)
        exit()
    if row[5] not in nats:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[5])
        print(row)
        exit()
    if row[7] not in manus:
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[7])
        print(row)
        exit()
    if re.match(inte, row[8]) == None and row[8] != "missing":
        print("")
        print("B2_ConverterHelpers.py chkRider(row) - 1")
        print(row[8])
        print(row)
        exit()

def chkLap(row):
    if len(row) != 13:
        print("")
        print("B2_ConverterHelpers.py chkLap(row) - 1")
        print(row)
        exit()

    if row[1] != "missing" and re.match(inte, row[1]) == None:
        print("")
        print("chkLap(row)")
        print("row[1]")
        print(row[1])
        exit()
    if re.match(lapTime, str(row[2])) == None and re.match(secTime, str(row[2])) == None and row[2] != "missing" and row[2] != "PIT" and row[2] != "unfinished":
        print("")
        print("chkLap(row)")
        print("row[2]")
        print(row[2])
        print(row)
        exit()
    if row[3] != "P" and row[3] != "did not pit" and row[3] != "missing":
        print("")
        print("chkLap(row)")
        print("row[3]")
        print(row[3])
        exit()

    for i in row[4:12]:
        if re.match(secTime, i) and re.match(lapTime, i) \
                and i == "no sec time" and i == "missing":
            print("")
            print("chkLap(row)")
            print("sec times")
            print(i)
            print(row)
            exit()

    if re.match(avgSpeed, row[12]) == None and row[12] != "missing":
        print("")
        print("chkLap(row)")
        print("row[12]")
        print(row[12])
        print(row)
        exit()

def chkRun(row):
    if len(row) != 6:
        print("B2_ConverterHelpers.py chkRun(row) - 1")
        print("row wrong length")
        print(row)
        exit()

    if re.match(inte, row[1]) == None and row[1] != "missing":
        print("B2_ConverterHelpers.py chkRun(row) - 2")
        print("row[1]")
        print(row[1])
        print(row)
        exit()


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

def getMatrix(rows, const):
    matrix = []
    if len(const) != 6:
        print("const length prob")
        print(f"len(const) = {len(const)}")
        exit()

    irider = ["position", "num", "fName", "lName", "nat", "team", "manu", "laps"]
    irun = ["runNum", "fTire", "rTire", "fAge", "rAge"]
    ilap = ["lapNum", "lapTime", "pitBoolean", "secTime", "secTime", "secTime", "secTime",
           "secTime", "secTime", "secTime", "secTime", "avgSpeed"]

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
            for l in lap: xLap.append(l)
            if len(xLap) != 30:
                print("xLap length problem")
                print(xLap)
                exit()
            matrix.append(xLap)
        else:
            print("B2_ConverterHelpers.py line 415")
            exit()





    return matrix























# def getFinFiles(type):
#     finFiles = []
#     with open(f"{sveDir}/{type}FinFiles.txt", "r") as f:
#         contents = f.readlines()
#         for i in contents:
#             finFiles.append(i)
#
#     for i in finFiles:
#         if i == 0 or i == []:
#             del i
#
#     print("finished files:")
#     if len(finFiles) == 0:
#         print("none")
#         y = finFiles
#     else:
#         y = finFiles[0].split("|")
#         for i in y:
#             print(i)
#
#     return y
#
# def formatRiderRow(row):
#     rider = ["-0-number-", "-1-f_name-", "-2-l_name-", "-3-manufacturer-", "-4-nation-",
#              "-5-team-", "-6-t_laps-", "-7-run_number-", "-8-f_Tire-", "-9-r_Tire-",
#              "-10-f_Age-", "-11-r_Age-", "-12-extra-"]
#     trash = ["MotoGP", "Tyre", "Moto2", "Moto3", "500cc", "125cc", "250cc"]
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#
#     x = 0
#     while x < len(row):
#         val = row[x]
#         if val in trash:
#             del row[x]
#         elif re.match(position, val):
#             del row[x]
#         elif val == "Total":
#             strLaps = row[x+1]
#             rider[6] = strLaps
#             del row[x:x+3]
#         elif val in nats:
#             rider[4] = val
#             del row[x]
#         elif val == "Run":
#             rider[7] = row[x+2]
#             del row[x:x+3]
#         elif val in manus:
#             rider[3] = val
#             del row[x]
#         else:
#             x += 1
#
#     x = 0
#     while x < len(row):
#         val = row[x]
#         if re.match("^\d{1,2}$", val) and rider[0] == "-0-number-":
#             rider[0] = val
#             del row[x]
#         else:
#             x += 1
#
#     x = 0
#
#     while x < len(row):
#         val = row[x]
#         if "Tyre" in val:
#             row[x] = val.replace("Tyre", "")
#         else:
#             x += 1
#
#     string = ""
#
#     for i in row:
#         val = i
#         string += f" {val}"
#     rider[-1] = string.strip()
#
#     return rider
#
# def rowAddRdrData(row, yr):
#     rData = getRidersData(yr)
#     found = False
#
#     print("")
#     rNum = row[0]
#     rNat = row[4]
#     rManu = row[3]
#     print(row)
#
#     while found == False:
#
#         for i in rData:
#             num = i[2]
#             name = i[3]
#             nat = i[4]
#             team = i[5]
#             m = i[6]
#             manu = m.upper()
#
#             if num == row[0]:
#                 print(i[2:])
#                 y = row[12].replace(name, "")
#                 row[12] = y.strip()
#                 x = name.split(" ", 1)
#                 row[1] = x[0]
#                 row[2] = x[1]
#                 row[5] = team
#                 found = True
#     del row[12]
#     row.insert(0, "rider")
#

#

#

#
# def fixRow(row):
#
#     inte = re.compile("^\d{1,2}$")
#     lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#     name = re.compile(
#         "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")
#     secTime = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}$")
#     avgSpeed = re.compile("^\d{2,3}[.]\d{1}$")
#
#     tires = ["Slick-Soft", "Slick-Medium", "Slick-Hard", "Wet-Soft", "Wet-Medium", "Wet-Hard", "missing"]
#     manus = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA", "KAWASAKI", "BMW", "TRIUMPH"]
#     nats = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
#             "AUT", "ARG", "CZE", "TUR"]
#
#     if row[0] == "lap":
#         if re.match(inte, row[1]) == None:
#             row.insert(1, "dnf")
#         if row[2] == "PIT":
#             row[2] = "unfinished"
#         if row[3] != "P":
#             row.insert(3, "did not pit")
#         else:
#             row[3] = "pit"
#         if re.match(avgSpeed, row[-1]) == None:
#             row.append("missing speed")
#         while len(row) != 13:
#             row.insert(-1, "no section time")
#
#     return row
#
# def chekRows(rows, file):
#     inte = re.compile("^\d{1,2}$")
#     lapTime = re.compile("^\d{1,2}[']\d\d[.]\d\d\d[*]{0,1}$")
#     position = re.compile("^\d{1,2}(st|nd|rd|th)$")
#     name = re.compile(
#         "^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$")
#     secTime = re.compile("^\d{1,2}[.]\d{3}[*]{0,1}$")
#     avgSpeed = re.compile("^\d{2,3}[.]\d{1}$")
#
#     tires = ["Slick-Soft", "Slick-Medium", "Slick-Hard", "Wet-Soft", "Wet-Medium", "Wet-Hard", "missing"]
#     manus = ["YAMAHA", "HONDA", "DUCATI", "SUZUKI", "KTM", "APRILIA", "KAWASAKI", "BMW", "TRIUMPH"]
#     nats = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR",
#             "AUT", "ARG", "CZE", "TUR"]
#
#     for i in rows:
#         if i[0] == "rider":
#             if len(i) != 13: print(f"{file}\n{i}")
#             if re.match(inte, i[1]) == None: print(f"{file}\n{i}")
#             if re.match(name, i[2]) == None: print(f"{file}\n{i}")
#             if re.match(name, i[3]) == None: print(f"{file}\n{i}")
#             if i[4] not in manus: print(f"{file}\n{i}")
#             if i[5] not in nats: print(f"{file}\n{i}")
#             if "laps=" not in i[7] and i[7] != "-6-t_laps-" : print(f"{file}\n{i}")
#
#             assert len(i) == 13
#             assert re.match(inte, i[1])
#             assert re.match(name, i[2])
#             assert re.match(name, i[3])
#             assert i[4] in manus
#             assert i[5] in nats
#             assert "laps=" in i[7] or i[7] == "-6-t_laps-"
#
#         elif i[0] == "run":
#             if len(i) != 6: print(f"{file}\n{i}")
#             if re.match(inte, i[1]) == None: print(f"{file}\n{i}")
#             if i[2] not in tires: print(f"{file}\n{i}")
#             if i[3] not in tires: print(f"{file}\n{i}")
#             if re.match(inte, i[4]) == None and i[4] != "missing": print(f"{file}\n{i}")
#             if re.match(inte, i[5]) == None and i[4] != "missing": print(f"{file}\n{i}")
#
#             assert len(i) == 6
#             assert re.match(inte, i[1])
#             assert i[2] in tires
#             assert i[3] in tires
#             assert re.match(inte, i[4]) or i[4] == "missing"
#             assert re.match(inte, i[5]) or i[4] == "missing"
#
#         elif i[0] == "lap":
#             if len(i) != 13: print(f"{file}\n{len(i)}\n{i}")
#             if re.match(inte, i[1]) == None and i[1] != "dnf": print(f"{file}\n{i}")
#             if re.match(lapTime, i[2]) == None and i[2] != "unfinished": print(f"{file}\n{i}")
#             if i[3] != "P" and i[3] != "did not pit" and i[3] != "pit": print(f"{file}\n{i}")
#             for j in i[4:-1]:
#                 if re.match(lapTime, j) == None and re.match(secTime, j) == None and j != "no section time":
#                     print("")
#                     print(j)
#                     print(f"{file}\n{i}")
#             if re.match(avgSpeed, i[-1]) == None and i[-1] != "missing speed": print(f"{file}\n{i}")
#
#             assert len(i) == 13
#             assert re.match(inte, i[1]) or i[1] == "dnf"
#             assert re.match(lapTime, i[2]) or i[2] == "unfinished"
#             assert i[3] == "P" or i[3] == "did not pit" or i[3] == "pit"
#             for j in i[4:-1]:
#                 assert re.match(lapTime, j) or re.match(secTime, j) or j == "no section time"
#             assert re.match(avgSpeed, i[-1]) or i[-1] == "missing speed"
#
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
# ########################################################################################################################
#

#

#

#

#
#
#
#
#
# def fixLapNum(row, lapNum):
#     try:
#         row[1] = int(row[1])
#     except:
#         passRow = True
#
#     if row[1] == lapNum:
#         passRow = True
#
#     elif row[1] == "unfinished":
#         row.insert(1, "0")
#
#     elif row[1] == "PIT":
#         row.insert(1, lapNum)
#
#     else:
#         print("\n\nrow[1] - stop")
#         print(row[1])
#         print(row)
#         print("\n")
#         exit()
#
#     return row
#
# def fixLapTime(row):
#     if re.match(lapTime, row[2]) or row[2] == "PIT" or row[2] == "unfinished": pass
#     elif re.match(secTime, row[2]): pass
#
#     else:
#         print("\n\nrow[2] - stop")
#         print(row[2])
#         print(row)
#         print("\n")
#         exit()
#
#     return row
#
# def fixLapPit(row):
#     if len(row) < 4:
#         row.append("no pit")
#         row.append("missing")
#         row.append("missing")
#
#     elif row[3] == "P":
#         passRow = True
#
#     elif row[3] == "b" or row[3] == "B":
#         row[3] = "P"
#
#     else:
#         row.insert(3, "no pit")
#
#     return row
#
# def fixAvgSpeed(row):
#     nuRow = []
#     nSplit = re.compile("\d[*]\d")
#
#     if re.match(avgSpeed, row[-1]):
#         nuAvgSpeed = row[-1]
#         del row[-1]
#     else: nuAvgSpeed = "missing"
#
#     for i in row[:4]:
#         nuRow.append(i)
#
#     if re.match(avgSpeed, row[-1]):
#         nuRow.append(row[-1])
#
#     else:
#         nuRow.insert(-1, "missing")
#
#     for i in row[4:]:
#         if re.match(secTime, i) or re.match(lapTime, i) or i == "missing":
#             nuRow.append(i)
#
#         elif re.match(nSplit, i):
#             j = i.split("*", 1)
#             k = j[0]
#             l = k + "*"
#             m = j[1]
#             nuRow.insert(-1, l)
#             nuRow.insert(-1, m)
#             frequency = 500
#             duration = 300
#             Beep(frequency, duration)
#
#         else:
#             print("\n\nrow[i] - stop")
#             print(i)
#             print(row)
#             print("\n")
#             exit()
#
#     nuRow.append(nuAvgSpeed)
#
#     return nuRow
#
# def fixSections(row):
#     while len(row) < 14:
#         row.insert(-1, "no sec time")
#
#     return row
#

#




