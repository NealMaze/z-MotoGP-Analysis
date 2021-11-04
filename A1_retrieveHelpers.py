# import necessary modules
from A2_ScrappingHelpers import *
from B2_ConverterHelpers import *
from D2_DataCleaningHelpers import *
from lists import *

def getRidersData(yr):
    data = []
    dataNue = []
    rows = []
    rem = ["'", "[", "]", '"']

    with open(f"{csvRidersDir}{yr}_Riders.csv", "r", encoding="utf8") as yrFile:
        i = csv.reader(yrFile, delimiter=",")
        for r in i:
            if r[0] != "f":
                rows.append(r)
        del rows[0]

    if len(rows[0]) < 3:
        for row in rows:
            x = []
            for i in row:
                k = i.split(",")
                for l in k:
                    werd = ""
                    for m in l:
                        if m not in rem:
                            werd = werd + m
                    x.append(werd)
            data.append(x)

    elif len(rows[0]) > 3:
        for row in rows:
            data.append(row)

    for i in data:
        p = []
        for j in i:
            x = j.strip()
            p.append(x)
        dataNue.append(p)

    return dataNue

def fixRidersData(yr):
    rs = []

    riders = getRidersData(yr)
    for i in riders:
        if len(i) not in rs:
            rs.append(len(i))

    df = pd.DataFrame(riders)
    df.to_csv(f"{csvRidersDir}{yr}RidersV2.csv", index = False, header = False)

def getRoundFiles(yr, rn, fileNum):
    base_url = 'http://www.motogp.com/en/Results+Statistics/'
    createdFiles = []

    eventWeather = []
    try:
        with open(f"{csvWeatherDir}{yr}_EventWeather.csv", "r", encoding = "utf8") as werkFile:
            i = csv.reader(werkFile, delimiter=",")
            for r in i:
                eventWeather.append(r)
            eventWeather.pop(0)
    except:
        wHeader = []
        wName = f"{csvWeatherDir}{yr}_EventWeather.csv"
        saveCSV(eventWeather, wName, wHeader)
        createdFiles.append(wName)

    seasonRiders = []
    try:
        with open(f"{csvRidersDir}{yr}_Riders.csv", "r", encoding = "utf8") as workFile:
            i = csv.reader(workFile, delimiter=",")
            for r in i:
                if r not in seasonRiders:
                    seasonRiders.append(r)
            seasonRiders.pop(0)
    except:
        rHeader = []
        rName = f"{csvRidersDir}{yr}_Riders.csv"
        saveCSV(seasonRiders, rName, rHeader)
        createdFiles.append(rName)

    if len(createdFiles) == 1:
        print("\ncreated file: ")
        for fName in createdFiles:
            print(fName)
    elif len(createdFiles) > 1:
        print("\ncreated files: ")
        for fName in createdFiles:
            print(fName)

    time.sleep(0 + np.random.random())
    TRK = rn['value']
    Track = rn['title']
    urlWk = base_url + yr + '/' + TRK + '/'
    soupWk = soup_special(urlWk)
    categories = get_all_cats(soupWk)
    print(f"\n    year:  {yr}")
    print(f"   round:  {fileNum}")
    xTrack = Track.split(" - ")
    print(f"   track:  {xTrack[1]}")

    for cat in categories:
        time.sleep(0 + np.random.random())
        CAT = cat.text
        url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
        soup_c = soup_special(url_c)
        sessions = get_all_sessions(soup_c)
        print(f"  league:  {CAT}")

        for ssn in sessions:
            time.sleep(0 + np.random.random())
            SSN = ssn
            if ssn == "RACE":
                SSN = "RAC"
            if ssn == "RACE1":
                SSN = "RAC1"
            if ssn == "RACE2":
                SSN = "RAC2"
            url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
            soupSSN = soup_special(url_ssn)
            pdfLinks = getPDFs(soupSSN)
            x = f"{SSN} - "
            if len(pdfLinks) == 0: x = x + "no PDFs found"

            # get weather and riders at session
            thisWeather, riders = getAllStats(soupSSN, yr, TRK, Track, CAT, SSN)
            if thisWeather not in eventWeather:
                eventWeather.append(thisWeather)

            for rider in riders:
                if rider not in seasonRiders:
                    seasonRiders.append(rider)

            for link in pdfLinks:
                time.sleep(1 + np.random.random())
                t = link.split("/")
                u = t[9].split(".")
                v = u[0]
                pdf = requests.get(link)
                fName = f"{pdfDir}{yr}-Round_{fileNum}-{CAT}-{Track}-{ssn}_{v}"
                with open(f"{fName}.pdf", "wb") as f:
                    f.write(pdf.content)
                    x = x + f"{v}, "
            print(x)

    wHeader = ["Year", "Date", "Track", "League", "Session_Type", "Track_Conditions", "Track_Temp", "Air_Temp", "Humidity"]
    yName = f"{csvWeatherDir}{yr}_EventWeather.csv"
    if eventWeather == "failed Weather":
        eventWeather = ["failed"]

    for weather in eventWeather:
        if weather == "failed Weather":
            weather = "failed"

    saveCSV(eventWeather, yName, wHeader)

    rHeader = ["Year", "League", "Number", "Name", "Nation", "Team", "Bike"]
    rName = f"{csvRidersDir}{yr}_Riders.csv"
    saveCSV(seasonRiders, rName, rHeader)
    fixRidersData(yr)

def grabFiles(yr, rnd):
    base_url = 'http://www.motogp.com/en/Results+Statistics/'

    url_yr = base_url + yr
    soupYr = soup_special(url_yr)
    rounds = getAllRounds(soupYr)

    intRnd = int(rnd)
    rndNdx = intRnd - 1

    rn = rounds[rndNdx]
    getRoundFiles(yr, rn, intRnd)

def getTestFiles(yr):
    yrUrl = "http://www.motogp.com/en/Results+Statistics/" + yr
    testSoup = soup_special(yrUrl)
    testLinks = getAllTests(testSoup, yr)
    testsCreated = []

    for link in testLinks:
        pdfSoup = soup_special(link)
        pdfLinks = getTestPDFs(pdfSoup)

        for pLink in pdfLinks:
            print(pLink)
            time.sleep(1 + np.random.random())
            j = pLink.split("/")
            k = j[-1].split(".")
            name =  k[0].replace(yr, "")

            pdf = requests.get(pLink)
            fName = f"{yr}{name}"
            with open(f"{pdfDir}{fName}.pdf", "wb") as f:
                f.write(pdf.content)
                testsCreated.append(fName)

    print("Tests Retrieved: ")
    for test in testsCreated: print(test)

def convertYrPdfs(yr, rnd):
    rootDir = "C:/Users/LuciusFish/Desktop/motoFiles/"
    pdfDir = (f"{rootDir}pdfFiles/")
    lges = ["MotoGP", "Moto2", "Moto3", "MotoE", "500cc", "250cc", "125cc"]
    badFiles = []

    for lge in lges:
        rcFiles = getFiles(pdfDir, f"{yr}*Round_{rnd}-*{lge}*nalysis.pdf")

        for file in rcFiles:
            fileName = file.replace(pdfDir, "")
            for i in ses:
                if i in file:
                    sesType = i
                    sesType = sesType.replace("_", "")

            if "RAC" in file:
                sesType = "RAC"
            if "RACE2" in file:
                sesType = "RAC2"
            if "RAC2" in file:
                sesType = "RAC2"
            if "RACE1" in file:
                sesType = "RAC1"

            saveName, track, round = getSaveName(file, sesType)
            col, date = openPDF(file)
            rows = parsePDF(col)

            month = date[0]
            month = month.lower()
            month = month.capitalize()
            day = date[1]
            rndNum = round.replace("Round_", "")
            id = f"{yr}-{lge}-{rndNum}-{sesType}-"

            const = ["const", month, day, yr, lge, round, sesType, track, ]
            chkConst(const, yr)

            rows.insert(0, const)

            cRows = getCRows(rows, yr, lge)

            for row in cRows:
                x = 0
                while x < len(row):
                    i = row[x]
                    j = str(i)
                    row[x] = j
                    x += 1

                if row[0] == "lap":
                    lapNum = chkLap(row, lapNum)
                elif row[0] == "rider":
                    lapNum = 0
                    chkRider(row, yr)
                elif row[0] == "run":
                    chkRun(row)
                else: exit("line 228")

            # for row in cRows:
            #     start = ""
            #     finish = ""
            #     qOne = ["Q1", "QP1"]
            #     qTwo = ["Q2", "QP_", "QP2", "EP"]
            #
            #     if row[6] == "RAC"
            #     row.insert(-1, start)

            matrix = getMatrix(cRows, const)
            mat = matFormat(matrix, id)
            secMat = processSeconds(mat)

            headers = ["index", "month", "day", "yr", "lge", "rnd", "session", "trk", "pos", "rdr_num", "f_name",
                       "l_name", "nat", "team", "manu", "num_of_laps", "run_num", "f_tire", "r_tire", "laps_on_f",
                       "laps_on_r", "lap_num", "lap_time", "lap_seconds", "lap_val", "pit", "sec_one",
                       "one_seconds", "one_val", "sec_two", "two_seconds", "two_val", "sec_thr", "thr_seconds",
                       "thr_val", "sec_four", "four_seconds", "four_val", "avg_spd"]
            xyz = saveName.replace(csvDir, "")
            print(xyz)
            saveCSV(secMat, saveName, headers)

            del rows
            del cRows
            del matrix

    if len(badFiles) > 0:
        print("\nFailed Files: ")
        for i in badFiles:
            print(i)

# combine years and leagues into separate files
def cleanData(yr, rnds):
    causeSes = ["Q2", "Q1", "QP-", "QP1", "QP2", "FP1", "FP2", "FP3", "FP4", "EP"]
    effectSes = ["RACE", "RACE1", "RACE2", "RAC", "RAC1", "RAC2"]

    for lge in lges:
        xLis = getFiles(csvSesDir, f"{yr}-{lge}-Round_*.csv")
        if len(xLis) > 0:
            print(f"\n         {yr} - {lge}")
        for rnd in rnds:
            trk = "none"
            gotQ = False

            Q1Res = []
            Q2Res = []
            files = getFiles(csvSesDir, f"{yr}-{lge}-Round_{rnd}-*.csv")
            if len(files) > 0:
                try:
                    grid = getGrid(yr, lge, rnd)
                    gdf = pd.DataFrame.from_dict(grid)
                    gotGrid = True
                except:
                    gotGrid = False

                causeFrames = []
                effectFrames = []

                for file in files:
                    df = pd.read_csv(file)
                    df["rdr_num"] = df["rdr_num"].astype(int)

                    oldNames = ["Losail International Circuit", "Autódromo Internacional do Algarve",
                                "Circuito de Jerez", "Autodromo Internazionale del Mugello", "Circuit de Barcelona",
                                "TT Circuit Assen", "Silverstone Circuit", "MotorLand Aragón", "Misano World Circuit",
                                "Circuit Of The Americas", "Automotodrom Brno", "Circuit Ricardo Tormo",
                                "Termas de Río Hondo", "Chang International Circuit", "Twin Ring Motegi",
                                "Sepang International Circuit", "Indianapolis Motor Speedway",
                                "Mazda Raceway Laguna Seca", "Estoril Circuit", "Donington Park Circuit",
                                "Shanghai Circuit", "Istanbul Circuit", "Style de Aragon", "Romagna"]
                    newNames = ["Losail", "Algarve", "Jerez", "Mugello", "Catalunya", "Assen", "Silverstone", "Aragon",
                                "Misano", "COTA", "Brno", "Valencia", "Argentina", "Chang", "Motegi", "Sepang",
                                "Indianapolis", "Laguna Seca", "Estoril", "Donington", "Shanghai", "Istanbul",
                                "Aragon", "Misano"]

                    x = 0
                    for name in oldNames:
                        oName = oldNames[x]
                        nName = newNames[x]
                        df.loc[df["trk"] == oName, "trk"] = nName
                        x = x + 1

                    trkDF = df["trk"]
                    trk = trkDF.iloc[0]

                    sesDF = df["session"]
                    session = sesDF.iloc[0]

                    bStrs = ["st", "nd", "rd", "th"]
                    for bStr in bStrs:
                        df["pos"] = df["pos"].map(lambda a: a.replace(bStr, ""))

                    appended = False

                    if gotGrid == True:
                        nueFrame = df
                    else:
                        nueFrame = df
                        if "Q2" in file:
                            Q2Res = getQRes(file)
                            if len(Q2Res) > 3:
                                gotQ = True
                        elif "QP2" in file:
                            Q2Res = getQRes(file)
                            if len(Q2Res) > 3:
                                gotQ = True
                        elif "QP-" in file:
                            Q2Res = getQRes(file)
                            if len(Q2Res) > 3:
                                gotQ = True

                        elif "Q1" in file:
                            Q1Res = getQRes(file)
                        elif "QP1" in file:
                            Q1Res = getQRes(file)

                        if gotQ == True:
                            grid = getWholeQRes(Q2Res, Q1Res)
                            gdf = pd.DataFrame.from_dict(grid)

                    rdrs = nueFrame.rdr_num.unique()
                    cols = ["lap_seconds", "one_seconds", "two_seconds", "thr_seconds", "four_seconds"]

                    for col in cols:
                        nueFrame[col] = pd.to_numeric(nueFrame[col], downcast = "float")
                        cleanCol = col.replace("_seconds", "_clean")
                        limCol = col.replace("_seconds", "_lim")
                        nueFrame[cleanCol] = nueFrame[col]
                        nueFrame[limCol] = nueFrame[col]

                        sesMin = df[cleanCol].min()
                        #
                        #
                        #
                        elif "lap" in col:
                            minDF = df.loc[df[cleanCol] < (sesMin + 30)]
                            lapStd = minDF[cleanCol].std()
                            twoStd = lapStd * 3
                            upLim = sesMin + twoStd
                        #
                        elif "RAC" in session:
                            minDF = df.loc[df[cleanCol] < (sesMin + 10)]
                            lapStd = minDF[cleanCol].std()
                            twoStd = lapStd * 3
                            upLim = sesMin + twoStd
                        #
                        else:
                            minDF = df.loc[df[cleanCol] < (sesMin + 20)]
                            lapStd = minDF[cleanCol].std()
                            thrStd = lapStd * 3
                            upLim = sesMin + thrStd
                        #
                        #
                        #
                        for rdr in rdrs:
                            sdf = nueFrame.loc[nueFrame["rdr_num"] == rdr]
                            tdf = sdf.loc[~sdf[cleanCol].isnull()]
                            udf = tdf.loc[tdf[cleanCol] < (sesMin + 20)]
                            rdrMean = udf[cleanCol].mean()
                            nueFrame[limCol] = upLim

                            if "RAC" not in session:
                                nueFrame.loc[nueFrame[col].isnull(), col] = rdrMean
                                seconds = nueFrame[col]
                                nueFrame.loc[(~nueFrame[col].isnull())
                                             & (nueFrame[col] <= nueFrame[limCol]),
                                             cleanCol] = seconds
                                nueFrame.loc[(~nueFrame[col].isnull())
                                             & (nueFrame[col] > nueFrame[limCol]),
                                             cleanCol] = upLim

                            else:
                                nueFrame.loc[(nueFrame[col].isnull())
                                             & (nueFrame["lap_num"] != 1),
                                             col] = rdrMean
                                seconds = nueFrame[col]
                                nueFrame.loc[(~nueFrame[col].isnull())
                                             & (nueFrame[col] <= nueFrame[limCol])
                                             & (nueFrame["lap_num"] != 1),
                                             cleanCol] = seconds
                                nueFrame.loc[(~nueFrame[col].isnull())
                                             & (nueFrame[col] > nueFrame[limCol])
                                             & (nueFrame["lap_num"] != 1),
                                             cleanCol] = upLim

                    nueFrame["lap_scaled"] = nueFrame["lap_clean"] / nueFrame["lap_clean"].abs().max()
                    nueFrame["one_scaled"] = nueFrame["one_clean"] / nueFrame["one_clean"].abs().max()
                    nueFrame["two_scaled"] = nueFrame["two_clean"] / nueFrame["two_clean"].abs().max()
                    nueFrame["thr_scaled"] = nueFrame["thr_clean"] / nueFrame["thr_clean"].abs().max()
                    nueFrame["four_scaled"] = nueFrame["four_clean"] / nueFrame["four_clean"].abs().max()

                    ### This would be a good place to more accurately normalize the first lap values
                    for ses in effectSes:
                        if ses in file:
                            firstFrame = nueFrame.loc[nueFrame["lap_num"] == 1]
                            for col in cols:
                                cleanCol = col.replace("_seconds", "_clean")
                                scaleCol = col.replace("_seconds", "_scaled")
                                seconds = firstFrame[col]
                                firstFrame.loc[~firstFrame[col].isnull(), cleanCol] = seconds
                                firstFrame[scaleCol] = firstFrame[cleanCol] / firstFrame[cleanCol].abs().max()
                                nueFrame.loc[nueFrame["lap_num"] == 1, scaleCol] = firstFrame[scaleCol]

                    nueFrame = nueFrame[["index", "month", "day", "yr", "lge", "rnd", "session", "trk", "pos",
                                         "rdr_num", "f_name", "l_name", "nat", "team", "manu", "num_of_laps", "run_num",
                                         "f_tire", "r_tire", "laps_on_f", "laps_on_r", "pit", "avg_spd",

                                         "lap_time", "lap_val",
                                         "sec_one", "one_val",
                                         "sec_two", "two_val",
                                         "sec_thr", "thr_val",
                                         "sec_four", "four_val",
                                         "lap_num",

                                         "lap_seconds", "lap_lim", "lap_clean", "lap_scaled",
                                         "one_seconds", "one_lim", "one_clean", "one_scaled",
                                         "two_seconds", "two_lim", "two_clean", "two_scaled",
                                         "thr_seconds", "thr_lim", "thr_clean", "thr_scaled",
                                         "four_seconds", "four_lim", "four_clean", "four_scaled"
                                         ]]

                    for ses in causeSes:
                        if ses in file:
                            if appended == False:
                                causeFrames.append(nueFrame)
                                appended = True

                    for ses in effectSes:
                        if ses in file:
                            if appended == False:
                                effectFrames.append(nueFrame)
                                appended = True

                if len(causeFrames) > 0:
                    cName = f"{yr}-{lge}-Rnd_{rnd}-{trk}-PreRace.csv"
                    cFrame = pd.concat(causeFrames)
                    dFrame = cFrame.join(gdf.set_index('rdr_num'), on='rdr_num')

                    dFrame.to_csv(f"{csvFinalDir}{cName}", index=False)

                if len(effectFrames) > 0:
                    eName = f"{yr}-{lge}-Rnd_{rnd}-{trk}-Result.csv"
                    eFrame = pd.concat(effectFrames)
                    fFrame = eFrame.join(gdf.set_index('rdr_num'), on='rdr_num')

                    fFrame.to_csv(f"{csvFinalDir}{eName}", index=False)

            if trk != "none":
                space = 20 - len(trk)
                x = " " * int(space)
                print(f"{x}{trk} - Round {rnd}")
