from lists import *
from jupyterHelpers import *
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import norm
import warnings
warnings.filterwarnings('ignore')

# %matplotlib inline

rnds = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20",
        "21", "22", "23", "24", "24"]

# combine years and leagues into separate files
def cleanData(uIn, year):
    if uIn != "y":
        yrs = [year]
    else:
        yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009",
               "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

    for yr in yrs:
        print(f"\n{yr}")
        for lge in lges:
            for rnd in rnds:
                rndFrames = []

                files = getFiles(csvSesDir, f"{yr}-{lge}-Round_{rnd}-*.csv")
                if len(files) > 0:
                    print(f"{yr} {lge}, round: {rnd}")

                    for file in files:
                        nf = pd.read_csv(file)

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
                    rndFr.to_csv(f"{csvFinalDir}{fName}", index=False)