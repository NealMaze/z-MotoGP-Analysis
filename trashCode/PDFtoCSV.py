# imports
from ProcessPdfHelpers import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")

yrs = ["2020"]
yr = yrs[0]

headers = ["Year", "Date", "League","TRK", "Track", "Session", "Track_Condition", "Track_Temp", "Air_Temp",
           "Humidity", "Position", "Rider_Number", "Rider_Name", "Team_Name", "Nationality", "Lap No.",
           "Lap_Valid", "Pit", "Lap_Time", "Section_1_Time", "Section_2_Time", "Section_3_Time", "Section_4_Time",
           "Section_5_Time", "Section_6_Time", "Section_7_Time", "Section_8_Time", "Avg_Speed"]

rcFiles = getRacAnalysis(yr, dir)

finFiles = []

def formatSession(cats):
    const = cats[0]

    const = []
    while len(cats[0]) != 0:
        const.append(cats[0][-1])
        del cats[0][-1]

    riders = cats[1]
    lapCnts = cats[2]
    nums = cats[3]
    laps = cats[4]

    x = 0
    for rider in riders:
        c = const
        rider.append(lapCnts[x])
        for i in nums[x]:
            rider.insert(0, i)
        x += 1

    for i in const:
        for rider in riders:
            rider.insert(0, i)

    for rider in riders:
        print(f"{rider[6]}, laps: {rider[-1]}")

for file in rcFiles[0:1]:
    print(file)
    cats = parseRacAnalysis(file)

    matrix = formatSession(cats)
    finFiles.append(file)