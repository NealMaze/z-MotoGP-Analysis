# imports
from ProcessPdfHelpers import *
# import PyPDF2 as p2
import re
import pdfplumber as plumb

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")

yrs = ["2020"]
yr = yrs[0]

headers = ["Year", "Date", "League","TRK", "Track", "Session", "Track_Condition", "Track_Temp", "Air_Temp",
           "Humidity", "Position", "Rider_Number", "Rider_Name", "Nationality", "Team_Name", "Lap No.",
           "Lap_Valid", "Pit", "Lap_Time", "Section_1_Time", "Section_2_Time", "Section_3_Time", "Section_4_Time",
           "Section_5_Time", "Section_6_Time", "Section_7_Time", "Section_8_Time", "Avg_Speed"]

pos = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
       "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
       "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]

rcFiles = getRacAnalysis(yr, dir)

def parseRacAnalysis(rc_file):
    pdf = plumb.open(rc_file)
    pages = pdf.pages
    const = getSessionConstants(pages)
    race = []
    rider_count = 0
    text = []









    for pg in pages:
        words = pg.extract_words()
        for i in words:
            text.append(i["text"])
            if i["text"] in pos:
                rider_count += 1
        stripBoilerPlate(text)

    rider = getRiderInfo(text, pos)
    getLaps(text, const, rider, race)

    pdf_num = 9
    for tb in text[pdf_num:30]:
        print(f"{pdf_num}     {tb}")
        pdf_num += 1

    for i in const:
        print(i)

    l = 1
    for lap in race:
        print(f"{l}   {lap}")
        l += 1

    print(f"Rider Count: {rider_count}")



for file in rcFiles[0:1]:
    print(file)

    parse = parseRacAnalysis(file)