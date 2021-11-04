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
            print(f"\n{yr} {lge}")
        for rnd in rnds:
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
                    race = False
                    if "RAC" in file:
                        race = True


                    df = pd.read_csv(file)
                    df['rdr_num'] = df['rdr_num'].astype(int)

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

                    rdrs = df.rdr_num.unique()

                    for rdr in rdrs:
                        cols = ["lap_seconds", "one_seconds", "two_seconds", "thr_seconds", "four_seconds"]
                        for col in cols:
                            iCol = col.replace("_seconds", "")
                            jCol = f"{iCol}_cleaned"
                            nueFrame[jCol] = nueFrame[col]

                            xdf = df.loc[df["rdr_num"] == rdr]
                            tdf = xdf.loc[~xdf[jCol].isnull()]

                            lapStd = tdf[jCol].std()
                            twoStd = lapStd * 2
                            lapMean = tdf[jCol].mean()
                            nueFrame[f"{jCol}_avg"] = lapMean
                            upLim = lapMean + twoStd

                            nueFrame.loc[(df["rdr_num"] == rdr) & (df[jCol] > upLim), jCol] = lapMean
                            ### droped this line because lower values should not be outliers
                            # nueFrame.loc[(df["rdr_num"] == rdr) & (df[col] < loLim), col] = loLim
                            xdf = df.loc[df["rdr_num"] == rdr]
                            tdf = xdf.loc[~xdf[col].isnull()]
                            lapMean = tdf[jCol].mean()
                            nueFrame.loc[(df["rdr_num"] == rdr) & (df[col].isnull()), col] = lapMean

                    nueFrame["lap_scaled"] = nueFrame["lap_seconds"] / nueFrame["lap_seconds"].abs().max()
                    nueFrame["one_scaled"] = nueFrame["one_seconds"] / nueFrame["one_seconds"].abs().max()
                    nueFrame["two_scaled"] = nueFrame["two_seconds"] / nueFrame["two_seconds"].abs().max()
                    nueFrame["thr_scaled"] = nueFrame["thr_seconds"] / nueFrame["thr_seconds"].abs().max()
                    nueFrame["four_scaled"] = nueFrame["four_seconds"] / nueFrame["four_seconds"].abs().max()

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
                    cName = f"{yr}-{lge}-Rnd_{rnd}-PreRace.csv"
                    cFrame = pd.concat(causeFrames)
                    dFrame = cFrame.join(gdf.set_index('rdr_num'), on='rdr_num')

                    oldNames = ["Losail International Circuit", "Autódromo Internacional do Algarve",
                                "Circuito de Jerez", "Autodromo Internazionale del Mugello", "Circuit de Barcelona",
                                "TT Circuit Assen", "Silverstone Circuit", "MotorLand Aragón", "Misano World Circuit",
                                "Circuit Of The Americas", "Automotodrom Brno", "Circuit Ricardo Tormo",
                                "Termas de Río Hondo", "Chang International Circuit", "Twin Ring Motegi",
                                "Sepang International Circuit", "Indianapolis Motor Speedway",
                                "Mazda Raceway Laguna Seca", "Estoril Circuit", "Donington Park Circuit",
                                "Shanghai Circuit", "Istanbul Circuit", "Style de Aragon"]
                    newNames = ["Losail", "Algarve", "Jerez", "Mugello", "Catalunya", "Assen", "Silverstone", "Aragón",
                                "Misano", "COTA", "Brno", "Valencia", "Argentina", "Chang", "Motegi", "Sepang",
                                "Indianapolis", "Laguna Seca", "Estoril", "Donington", "Shanghai", "Istanbul",
                                "Aragón"]

                    x = 0
                    for name in oldNames:
                        oName = oldNames[x]
                        nName = newNames[x]
                        dFrame.loc[dFrame["trk"] == oName, "trk"] = nName
                        x = x + 1

                    dFrame.to_csv(f"{csvFinalDir}{cName}", index=False)
                    print(cName)

                if len(effectFrames) > 0:
                    eName = f"{yr}-{lge}-Rnd_{rnd}-Result.csv"
                    eFrame = pd.concat(effectFrames)
                    fFrame = eFrame.join(gdf.set_index('rdr_num'), on='rdr_num')

                    oldNames = ["Losail International Circuit", "Autódromo Internacional do Algarve",
                                "Circuito de Jerez", "Autodromo Internazionale del Mugello", "Circuit de Barcelona",
                                "TT Circuit Assen", "Silverstone Circuit", "MotorLand Aragón", "Misano World Circuit",
                                "Circuit Of The Americas", "Automotodrom Brno", "Circuit Ricardo Tormo",
                                "Termas de Río Hondo", "Chang International Circuit", "Twin Ring Motegi",
                                "Sepang International Circuit", "Indianapolis Motor Speedway",
                                "Mazda Raceway Laguna Seca", "Estoril Circuit", "Donington Park Circuit",
                                "Shanghai Circuit", "Istanbul Circuit"]
                    newNames = ["Losail", "Algarve", "Jerez", "Mugello", "Catalunya", "Assen", "Silverstone", "Aragón",
                                "Misano", "COTA", "Brno", "Valencia", "Argentina", "Chang", "Motegi", "Sepang",
                                "Indianapolis", "Laguna Seca", "Estoril", "Donington Park", "Shanghai", "Istanbul"]

                    x = 0
                    for name in oldNames:
                        oName = oldNames[x]
                        nName = newNames[x]
                        fFrame.loc[fFrame["trk"] == oName, "trk"] = nName
                        x = x + 1

                    fFrame.to_csv(f"{csvFinalDir}{eName}", index=False)
                    print(eName)