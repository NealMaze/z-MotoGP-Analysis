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
  
def mergeWeather(df):
    weatherFiles = getFiles(csvWeatherDir, f"*.csv")
    weatherFrames = []

    for file in weatherFiles:
        weatherFrame = pd.read_csv(file)
        weatherFrames.append(weatherFrame)

    wf = pd.concat(weatherFrames)
    wf = wf[wf["Year"].notna()]
    wf = wf[wf.Year != "f"]
    wf["Year"] = wf["Year"].astype(int)
    wf.columns = wf.columns.str.lower()

    dateData = wf["date"].str.split(",", n=2, expand=True)
    wf["month"] = dateData[0]
    wf["day"] = dateData[1]
    wf["yr"] = dateData[2]
    wf.drop(columns=["date", "track", "year"], inplace=True)

    wf = wf[["month", "day", "yr", "league", "session_type", "track_conditions", "track_temp", "air_temp", "humidity"]]
    wf = wf.rename(columns={"league": "lge", "session_type": "session", "track_conditions": "conditions"})
    wf["yr"] = wf["yr"].astype(int)
    wf["day"] = wf["day"].astype(int)

    df["yr"] = df["yr"].astype(int)
    df["day"] = df["day"].astype(int)
    df["result"] = df["result"].astype(int)

    wholeFrame = pd.merge(df, wf, how = "left",
                          left_on = ["month", "day", "yr", "lge", "session"],
                          right_on = ["month", "day", "yr", "lge", "session"])

    return wholeFrame

def getWholeFrame(pas, df, yr):
    prob = False
    if pas == "empty":
        retFrames = []
        pas = "full"
    else:
        retFrames = [df]

    frames = []

    for lge in lges:
        for rnd in rnds:
            preFiles = getFiles(csvFinalDir, f"{yr}-{lge}-Rnd_{rnd}-*-PreRace.csv")
            resFiles = getFiles(csvFinalDir, f"{yr}-{lge}-Rnd_{rnd}-*-Result.csv")

            if len(resFiles) > 0:
                resFile = resFiles[-1]
                if len(resFiles) > 1:
                    print("")
                    for i in resFiles: print(i)
                    print("")
                    print(resFile)
                    print("")

            if len(preFiles) > 1:
                print("\nproblem\n\nproblem\n\nproblem\n\nproblem\n\n")
                prob = True
            if len(preFiles) > 0:
                preFile = preFiles[0]
                preFrame = pd.read_csv(preFile)

                if len(resFiles) > 0:
                    resFrame = pd.read_csv(resFile)
                    sessions = resFrame.session.unique()
                    finRac = sessions[-1]
                    resSmolFrame = resFrame.loc[(resFrame["session"] == finRac)]
                    sessions = resSmolFrame.session.unique()
                    if len(sessions) > 1:
                        print(f"\n{yr} {lge} rnd_{rnd}")
                        print(sessions)

                    rdrFrame = resSmolFrame[["rdr_num", "pos"]]
                    rdrFrame = rdrFrame.drop_duplicates()
                    rdrFrame = rdrFrame.rename(columns={"pos": "result"})
                    nFrame = preFrame.join(rdrFrame.set_index("rdr_num"), on="rdr_num")
                    val = {"result": 100}
                    nF = nFrame.fillna(value=val)

                    try:
                        nF["start_pos"] = nF["start_pos"].astype(int)
                    except:
                        pass

                else:
                    preFrame["result"] = 100
                    nF = preFrame

                frames.append(nF)

    wF = pd.concat(frames)
    wF = wF[wF.result != "0-pos"]
    if prob == True: print("\nproblem\n\nproblem\n\nproblem\n\nproblem\n\n")

    retFrames.append(wF)
    wF = pd.concat(retFrames)

    return wF, pas

def getResFrame(df, yr):
    frames = []
    if df == "empty": pass
    else: frames.append(df)


    for lge in lges:
        for rnd in rnds:
            resFiles = getFiles(csvFinalDir, f"{yr}-{lge}-Rnd_{rnd}-*-Result.csv")
            for file in resFiles:
                df = pd.read_csv(file)
                frames.append(df)

    df = pd.concat(frames)
    return df
