# imports
from A1_retrieveHelpers import *
from lists import *

def getFiles(dir, string):
    # gets Files from the provided dir matching the provided string
    filterFiles = fnmatch.filter(listdir(dir), f"{string}")
    files = [f"{dir}{file}" for file in filterFiles]
    return files

def toSecs(receive):
    strings = ["unfinished", "PIT"]

    if isinstance(receive, float):
        ret = receive

    elif receive in strings:
        ret = None

    else:
        receive = receive.replace("*", "")
        totSec = 0

        if ":" in receive:
            hours, receive = receive.split(':')
            totSec += int(hours) * 3600

        if "'" in receive:
            minutes, receive = receive.split("'")
            totSec += int(minutes) * 60

        totSec += float(receive)
        ret = totSec

    return ret

def updateSes(yr, rnds):
    for rnd in rnds:
        grabFiles(yr, rnd)
        convertYrPdfs(yr, rnd)
        cleanData(yr, rnds)

def getWholeFrame():
    files = getFiles(csvFinalDir, "*.csv")
    frames = []

    for file in files:
        df = pd.read_csv(file)
        frames.append(df)

    wholeFrame = pd.concat(frames)
    newFrame = wholeFrame.drop(["pos", "lap_val", "lap_time", "sec_one", "one_val", "sec_two", "two_val", "sec_thr",
                                "thr_val", "sec_four", "four_val"], axis = 1)

    return newFrame
