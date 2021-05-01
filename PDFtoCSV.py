# imports
from ProcessPdfHelpers import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")

yrs = ["2020"]
yr = yrs[0]

headers = ["Year", "Date", "League","TRK", "Track", "Session", "Track_Condition", "Track_Temp", "Air_Temp",
           "Humidity", "Position", "Rider_Number", "Rider_Name", "Nationality", "Team_Name", "Lap No.",
           "Lap_Valid", "Pit", "Lap_Time", "Section_1_Time", "Section_2_Time", "Section_3_Time", "Section_4_Time",
           "Section_5_Time", "Section_6_Time", "Section_7_Time", "Section_8_Time", "Avg_Speed"]

rcFiles = getRacAnalysis(yr, dir)

finFiles = []

def parseRacAnalysis(rc_file):
    pdf = plumb.open(rc_file)
    pages = pdf.pages
    const = getSessionConstants(pages)
    session = []
    sheets, endSig = getTxt(pages)

    finRiderCount = 0

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

    sheetCount = 0
    for sheet in sheets:
        sheetCount += 1
        side = 0
        while sheet[0] != endSig:
            row, var = runRow(sheet)
            cat = getCat(side, cats, var)
            cat.append(row)
            side += 1
        cats = emptyOddLists(cats)
        print(f"sheet number: {sheetCount}")

    for rider in ridOd:
        print(rider)












for file in rcFiles[0:1]:
    print(file)

    parse = parseRacAnalysis(file)