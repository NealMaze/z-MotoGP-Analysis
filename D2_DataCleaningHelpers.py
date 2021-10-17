from lists import *
from jupyterHelpers import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

from B2_ConverterHelpers import getFiles
from C2_GridConverterHelpers import *

# %matplotlib inline

rnds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "24"]


# def getStartPositions(yr, lge, rnd):
#     rnds = [rnd]
#
#     for rnd in rnds:
#         grdFiles3 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*EP_Session.pdf")
#         grdFiles2 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*QP_Session.pdf")
#         grdFiles = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*QualifyingResults.pdf")
#         for file in grdFiles2: grdFiles.append(file)
#         for file in grdFiles3: grdFiles.append(file)
#
#         if len(grdFiles) == 1:
#             for file in grdFiles:
#                 page = openGridPDF(file)
#                 page = stripHeader(page)
#                 page = getRows(page)
#                 page = stripFooter(page)
#                 page = stripExtra(page)
#                 page = lowerCase(page)
#
#             return page
#
#         elif len(grdFiles) > 1:
#             print("\n\n\nProblem")
#             print(f"{yr} {lge} {rnd}")
#             for i in grdFiles:
#                 print(i)
#             print("\n\n\n")
#             return "nope"
#
#         else:
#             return "no files"

# calculates start positions from Qualifying CSVs
def getQRes(file):
    QRes = []

    with open(file, "r", encoding="utf8") as csvFile:
        i = csv.reader(csvFile, delimiter=",")
        for r in i:
            QRes.append(r)

    results = []
    rdrs = []
    conts = ["st", "nd", "rd", "th"]

    for i in QRes:
        if i[9] not in rdrs:
            position = i[8]

            posit = [i[9], position]
            rdrs.append(i[9])
            results.append(posit)

    nRows = []
    for i in results:
        x2 = i[1]
        for cont in conts:
            if cont in x2:
                x2 = x2.replace(cont, "")
        newRow = [x2, i[0]]
        nRows.append(newRow)

    del QRes
    del rdrs
    nRows.pop(0)

    return nRows

# combine results from Q1 and Q2
def getWholeQRes(Q2Res, Q1Res):
    rdrs = []
    line = []

    for i in Q2Res:
        rdrs.append(i[0])
        rdrs.append(i)

    if len(Q2Res) > 0:
        q = Q2Res[-1][1]
        r = int(q)
        x = r + 1
        for i in Q1Res:
            rdrNum = i[0]
            if rdrNum not in rdrs:
                rdrs.append(rdrNum)
                pos = x
                line = [rdrNum, pos]
                Q2Res.append(line)
                x = x + 1

    nPos = []
    nRdr = []
    for i in Q2Res:
        nPos.append(int(i[0]))
        nRdr.append(int(i[1]))

    grid = {"start_pos": nPos, "rdr_num": nRdr}

    return grid

# gets start positions from pdf files
def getGrid(yr, lge, rnd):
    grdFiles = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}-*RACE_LapChart.pdf")
    grdFiles2 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}-*RACE2_LapChart.pdf")

    if len(grdFiles2) > 0:
        grdFiles = grdFiles2

    if len(grdFiles) > 1:
        print("\n\n\nProblem")
        for i in grdFiles:
            print(i)
        print("\n\n\n")

    for file in grdFiles:
        saveName = f"{yr}-{lge}-Round_{rnd}-StartGrid.csv"

        page = openGridPDF(file)
        page = stripHeader(page)
        lenPos, position = getPos(page)
        lenNum, rider = getNum(page)

    position.pop(0)
    position.pop(0)
    rider.pop(0)
    rider.pop(0)

    nPos = []
    nRdr = []
    for i in position:
        nPos.append(int(i))
    for i in rider:
        nRdr.append(int(i))

    grid = {"start_pos": nPos, "rdr_num": nRdr}

    if len(position) < 2:
        grid = "none"

    return grid
