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

# gets start positions from pdf files
def getStartPositions(yr, lge, rnd):
    rnds = [rnd]

    for rnd in rnds:
        grdFiles3 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*EP_Session.pdf")
        grdFiles2 = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*QP_Session.pdf")
        grdFiles = getFiles(pdfDir, f"{yr}-Round_{rnd}-{lge}*QualifyingResults.pdf")
        for file in grdFiles2: grdFiles.append(file)
        for file in grdFiles3: grdFiles.append(file)

        if len(grdFiles) == 1:
            for file in grdFiles:
                page = openGridPDF(file)
                page = stripHeader(page)
                page = getRows(page)
                page = stripFooter(page)
                page = stripExtra(page)
                page = lowerCase(page)

            return page

        elif len(grdFiles) > 1:
            print("\n\n\nProblem")
            print(f"{yr} {lge} {rnd}")
            for i in grdFiles:
                print(i)
            print("\n\n\n")
            return "nope"

        else:
            return "no files"

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

    return Q2Res

#

# combine years and leagues into separate files
def cleanData(yr, rnds):
        print(f"\n{yr}")
        for lge in lges:
            for rnd in rnds:
                rndFrames = []

                files = getFiles(csvSesDir, f"{yr}-{lge}-Round_{rnd}-*.csv")
                if len(files) > 0:
                    for file in files:
                        # this creates a dataframe
                        nf = pd.read_csv(file)

                        Q2Res = []
                        if "Q2" in file:
                            Q2Res = getQRes(file)

                        Q1Res = []
                        if "Q1" in file:
                            Q1Res = getQRes(file)

                        grid = []
                        if len(Q2Res) > 0:
                            grid = getWholeQRes(Q2Res, Q1Res)

                        if "QP" in file:
                            grid = getQRes(file)

                        sName = file.split("-")
                        fName = f"{yr}-{lge}-{sName[2]}-{sName[3]}.csv"

                        # get list of rider numbers in session
                        rdrs = nf.rdr_num.unique()
                        frames = []

                        for rdr in rdrs:
                            rdrFrame = nf[nf["rdr_num"] == rdr]



                            avgSpeed = rdrFrame["avg_spd"].mean()
                            avgLap = rdrFrame["lap_seconds"].mean()
                            avgOne = rdrFrame["one_seconds"].mean()
                            avgTwo = rdrFrame["two_seconds"].mean()
                            avgThr = rdrFrame["thr_seconds"].mean()
                            avgFour = rdrFrame["four_seconds"].mean()

                            # fillna with the average values
                            _ = rdrFrame.fillna(
                                {"lap_seconds": avgLap, "one_seconds": avgOne, "two_seconds": avgTwo, "thr_seconds": avgThr,
                                 "four_seconds": avgFour, "avg_spd": avgSpeed}, inplace=True)

                            # append created rider frame to nueFrame
                            frames.append(rdrFrame)

                        sesFrame = pd.concat(frames)

                        sesFrame["start"] = np.nan

                        # create normalized columns for lap time, section times, and top speed
                        sesFrame["lap_scaled"] = sesFrame["lap_seconds"] / sesFrame["lap_seconds"].abs().max()
                        sesFrame["one_scaled"] = sesFrame["one_seconds"] / sesFrame["one_seconds"].abs().max()
                        sesFrame["two_scaled"] = sesFrame["two_seconds"] / sesFrame["two_seconds"].abs().max()
                        sesFrame["thr_scaled"] = sesFrame["thr_seconds"] / sesFrame["thr_seconds"].abs().max()
                        sesFrame["four_scaled"] = sesFrame["four_seconds"] / sesFrame["four_seconds"].abs().max()
                        sesFrame["avgSpd_scaled"] = sesFrame["avg_spd"] / sesFrame["avg_spd"].abs().max()

                        if "RAC" not in file:
                            sesFrame["results"] = np.nan
                        else:
                            sesFrame["results"] = sesFrame["pos"]

                        rndFrames.append(sesFrame)

                    rndFr = pd.concat(rndFrames)

                    rdrs = rndFr.rdr_num.unique()
                    frames = []

########################################################################################################################
                    # check if grid value is valid
                    # if grid value is not valid
                    # use:
                    # getStartPositions(yr, lge, rnd)
                    # function to retrieve start positions from other PDF file
########################################################################################################################

                    for rdr in rdrs:
                        intRdr = int(rdr)
                        rdrStartPos = ""

                        for place in grid:
                            intPlace = place[1]
                            try:
                                iP = int(intPlace)
                            except:
                                iP = ""
                            if intRdr == iP:
                                rdrStartPos = place[0]

                        rdrFrame = rndFr[rndFr["rdr_num"] == rdr]

                        rdrFrame["start"] = rdrFrame["start"].fillna(rdrStartPos)
                        rdrFrame["results"] = rdrFrame["results"].fillna(method="bfill")
                        rdrFrame["results"] = rdrFrame["results"].fillna(method="ffill")

                        frames.append(rdrFrame)

                    rndFrame = pd.concat(frames)
                    print(fName)
                    rndFrame.to_csv(f"{csvFinalDir}{fName}", index = False)
