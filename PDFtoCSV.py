# imports
from ProcessPdfHelpers import *
import PyPDF2 as p2

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")

yrs = ["2020"]
yr = yrs[0]

headers = ["Year", "Date", "League","TRK", "Track", "Session", "Track_Condition", "Track_Temp", "Air_Temp",
           "Humidity", "Position", "Rider_Number", "Rider_Name", "Nationality", "Team_Name", "Lap No.",
           "Lap_Valid", "Pit", "Lap_Time", "Section_1_Time", "Section_2_Time", "Section_3_Time", "Section_4_Time",
           "Section_5_Time", "Section_6_Time", "Section_7_Time", "Section_8_Time", "Avg_Speed"]

rcFiles = getRaceFiles(yr, dir)

def parseRacPDF(file):
    headers = ["Year", "Date", "League", "TRK", "Track", "Session", "Rider_Number", "Rider_Name", "Nationality",
               "Team_Name", "Lap No.", "Lap_Valid", "Pit", "Lap_Time", "Section_1_Time", "Section_2_Time",
               "Section_3_Time", "Section_4_Time", "Section_5_Time", "Section_6_Time", "Section_7_Time",
               "Section_8_Time", "Avg_Speed"]
    pg_count = 0
    pdfFile = open(file, "rb")
    read = p2.PdfFileReader(pdfFile)
    pg = read.getPage(pg_count)
    fst_page = (pg.extractText())
    fst_page.strip("""TISSOT""")

    print("\n")
    print(fst_page + "END")

    year = ""
    date = ""
    league = ""
    TRK = ""
    track = ""
    session = ""
    laps = ""

    # for page in read.getNumPages():
    #     pg = read.getPage(pg_count)
    #     pages.append(pg)
    #     pg_count += 1
    # for page in pages:
        # strip boilerplate
        # append to

    # create dictionary
    # create dataframe
    # strip unnecessary opening boilerplate
    # split by rider
    # for rider: process, then append to dataframe
    # return dataframe

    # return pg_count


for file in rcFiles[0:1]:
    print(file)

    parse = parseRacPDF(file)