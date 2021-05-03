# imports
from ProcessPdfHelpers import *

dir = ("C:/Users/LuciusFish/Desktop/MotoGP_PDFs/Analysis")

yrs = ["2020"]
yr = yrs[0]

def parsePDF(rc_file):
    sheets, const = openPDF(rc_file)

    for sheet in sheets:
        sideOne = []
        sideTwo = []
        








########################################################################################################################
########################################################################################################################
########################################################################################################################
for file in rcFiles[0:1]:
    print(file)
    cats = parsePDF(file)

    finFiles.append(file)