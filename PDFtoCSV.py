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

def parseRacAnalysis(rc_file):
    pdf = plumb.open(rc_file)
    pages = pdf.pages
    const = getSessionConstants(pages)
    session = []
    text, pos = getTxt(pages)

    for i in text:
        if type(i) is in



    # rider = getRiderInfo(text, pos[0])
    # pos.remove(pos[0])
    # getLaps(text, const, rider, session)

    pdf_num = 0
    for tb in text[pdf_num:20]:
        print(f"{pdf_num}     {tb}")
        pdf_num += 1

    # for i in pos:
    #     rider = getRiderInfo(text, pos[0])
    #     pos.remove(pos[0])
    #     getLaps(text, const, rider, session)
    #     pos.remove(pos[0])









#     for i in const:
#         print(i)
#
#     l = 1
#     for lap in race:
#         print(f"{l}   {lap}")
#         l += 1
#
#     print(f"Rider Count: {rider_count}")



for file in rcFiles[0:1]:
    print(file)

    parse = parseRacAnalysis(file)