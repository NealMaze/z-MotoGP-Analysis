# imports
from os import listdir
import pdfplumber as plumb
import fnmatch

def openPDF(rcFile):
    pdf = plumb.open(rcFile)
    pages = pdf.pages
    const = getSessionConstants(pages)
    sheets = getSheets(pages)

    return sheets, const

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

def getSheets(pages):
    positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
                 "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
                 "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]

    sheets = []

    for pg in pages:
        sheet = []
        words = pg.extract_words()

        stripBoilerPlate(words)
        for i in words:
            sheet.append(i)
        sheets.append(sheet)

    return sheets










