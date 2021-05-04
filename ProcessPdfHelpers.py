# imports
from os import listdir
import pdfplumber as plumb
import fnmatch

def parseRacAnalysis(rc_file):
    pdf = plumb.open(rc_file)
    pages = pdf.pages
    const = getSessionConstants(pages)
    sheets, endSig = getTxt(pages)

    riderCount = getRiderCount(sheets)

    # for sheet in sheets:

    ridEv = []
    ridOd = []
    rid = [ridEv, ridOd]
    lapCntEv = []
    lapCntOd = []
    lapCnt = [lapCntEv, lapCntOd]
    lapEv = []
    lapOd = []
    laps = [lapEv, lapOd]
    numEv = []
    numOd = []
    nums = [numEv, numOd]
    cats = [rid, lapCnt, nums, laps]
    columns = []

    sheetCount = 0
    for sheet in sheets:
        tripWire = 1
        sheetCount += 1
        side = 4
        while sheet[0] != endSig:
            row, var = runRow(sheet,tripWire)

            ###########################################################################################
            # if riderCount > 0:
            #     side += 1
            # if var == "num":
            #     if int(row[0]) == riderCount:
            #         riderCount = 0
            #
            #
            # if riderCount == 0:
            #     if var == "bLap":
            #         tripWire = 0
            #         sid = 2
            ###############################################################################################

            cat = getCat(side, cats, var)
            cat.append(row)
        cats = emptyEvenLists(cats)

    emts = []
    emts.append(const)

    for i in cats:
        emts.append(i[1])

    return emts

def getRacAnalysis(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rcFiles = [f"{dir}/{file}" for file in filter_files]
    return rcFiles

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

def getTxt(pages):
    sheets = []
    endSig = "End_Page - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -"
    positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
                 "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
                 "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]

    for pg in pages:
        words = pg.extract_words()
        txt = []
        sheet = []
        for i in words:
            txt.append(i["text"])

        stripBoilerPlate(txt)
        for t in txt:
            sheet.append(t)

        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)
        sheet.append(endSig)

        x = 0
        for i in sheet:
            if sheet[x] == "*":
                sheet[x-1] += " *"
                del sheet[x]
            elif sheet[x] == "P":
                sheet[x-1] += " P"
                del sheet[x]
            else:
                x += 1
        sheets.append(sheet)

    return sheets, endSig

def getRiderCount(sheets):
    r = 0
    for sheet in sheets:
        for word in sheet:
            if word == "Full":
                r += 1

    return r

def stripBoilerPlate(lis):
    x = 0
    while "Speed" not in lis[x]:
        x += 1
    x += 1
    del lis[0:x]
    x = 0
    while "Speed" not in lis[x]:
        x += 1
    x += 1
    del lis[0:x]
    end_index = lis.index("Fastest")
    del lis[end_index:]

def getCats():
    ridEv = ["even riders"]
    ridOd = ["odd riders"]
    rid = [ridEv, ridOd]
    posEv = ["even positions"]
    posOd = []
    pos = [posEv, posOd]
    lapCntEv = []
    lapCntOd = []
    lapCnt = [lapCntEv, lapCntOd]
    lapEv = []
    lapOd = []
    laps = [lapEv, lapOd]
    numEv = []
    numOd = []
    nums = [numEv, numOd]
    cats = [rid, pos, lapCnt, nums, laps]

    return cats

def runRow(lis, rcnt):
    var = "lap"
    bLaps = ["unfinished", "PIT"]
    positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
                 "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
                 "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]
    rLis = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37",
            "39", "40"]

    if int(rcnt) == 0:
        row = None
        var = "lap"

    elif "Runs=" in lis[0]:                               # Lap Count
        strLaps = lis[2]
        row = strLaps.replace("laps=", "")
        var = "lapNum"
        del lis[:5]

    elif lis[0] in bLaps:                               # Bad Laps
        row = getBadLap(lis)
        var = "bLap"

    elif str(lis[0]) in rLis:                           # Good Laps
        row = getGoodLap(lis)

    elif lis[0] in positions:                           # Rider Number
        row = getNumber(lis)
        var = "num"

    elif type(lis[0]) == str:                           # Rider Info
        row = getRider(lis)
        var = "rider"

    return row, var

def getCat(side, cats, var):
    if var == "rider":
        x = 0
    elif var == "lapNum":
        x = 1
    elif var == "num":
        x = 2
    elif var == "lap":
        x = 3
    elif var == "bLap":
        x = 3

    y = 0
    if (side % 2) != 0:
        y = 1

    return cats[x][y]

def getRider(lis):
    rider = []
    rider.append(f"{lis[0]} {lis[1]}")
    del lis[0:2]
    team, nat = getRiderTeam(lis)
    rider.append(team)
    rider.append(nat)

    return rider

def getRiderTeam(lis):
    nations = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR"]
    ls = []
    team = ""
    x = 0

    while lis[x] not in nations:
        ls.append(lis[x])
        x += 1

    del lis[:x]
    nat = lis[0]
    for i in ls:
        j = f" {i}"
        team += j
    del lis[0]

    return team, nat

def getNumber(lis):
    z = lis[0]
    z = z[:-2]
    num = lis[1]
    t = []
    t.append(z)
    t.append(num)
    del lis[:2]

    return t

def getBadLap(lis):
    lap = []
    lap.append(None)
    lap.append(lis[0])
    del lis[0]
    while len(lap) < 6:
        if float(lis[0]) < 100:
            lap.append(lis[0])
            del lis[0]
        else:
            lap.append(None)
    if float(lis[0]) > 100:
        lap.append(lis[0])
        del lis[0]
    else:
        lap.append(None)
        del lis[0]
    return lap

def getGoodLap(lis):
    lap = []
    for i in lis[:7]:
        lap.append(i)
    del lis[:7]

    return lap

def emptyEvenLists(cats):
    x = 0
    y = 0
    for cat in cats:
        for i in cat[0]:
            cat[1].append(i)
        cat[0] = []
    return cats

