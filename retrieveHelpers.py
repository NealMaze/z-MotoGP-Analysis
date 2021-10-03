# import necessary modules
from A2_ScrappingHelpers import *
from B2_ConverterHelpers import *
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
    saveCSV(eventWeather, yName, wHeader)

    rHeader = ["Year", "League", "Number", "Name", "Nation", "Team", "Bike"]
    rName = f"{csvRidersDir}{yr}_Riders.csv"
    saveCSV(seasonRiders, rName, rHeader)
    fixRidersData(yr)

def grabFiles(yr, rnds):
    base_url = 'http://www.motogp.com/en/Results+Statistics/'

    url_yr = base_url + yr
    soupYr = soup_special(url_yr)
    rounds = getAllRounds(soupYr)
    for rnd in rnds:

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

def convertYrPdfs(yr):
    rootDir = "C:/Users/LuciusFish/Desktop/motoFiles/"
    pdfDir = (f"{rootDir}pdfFiles/")
    lges = ["MotoGP", "Moto2", "Moto3", "MotoE", "500cc", "250cc", "125cc"]
    badFiles = []


    for lge in lges:
        rcFiles = getFiles(pdfDir, f"{yr}*Round_*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print(f"\n{lge}")

        for file in rcFiles:
            fileName = file.replace(pdfDir, "")
            print(fileName)
            # try:
            for i in ses:
                if i in file:
                    sesType = i
                    sesType = sesType.replace("_", "")
                    sesType = sesType.replace("RACE2", "RAC2")

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

            matrix = getMatrix(cRows, const)
            mat = matFormat(matrix, id)
            secMat = processSeconds(mat)

            headers = ["index", "month", "day", "yr", "lge", "rnd", "session", "trk", "pos", "rdr_num", "f_name",
                       "l_name", "nat", "team", "manu", "num_of_laps", "run_num", "f_tire", "r_tire", "laps_on_f",
                       "laps_on_r", "lap_num", "lap_time", "lap_seconds", "lap_val", "pit", "sec_one",
                       "one_seconds", "one_val", "sec_two", "two_seconds", "two_val", "sec_thr", "thr_seconds",
                       "thr_val", "sec_four", "four_seconds", "four_val", "avg_spd"]
            saveCSV(secMat, saveName, headers)

            del rows
            del cRows
            del matrix

            # except:
            #     print(f"\nFailed Parsing:\n{fileName}\n")
            #     badFiles.append(fileName)

    if len(badFiles) > 0:
        print("\nFailed Files: ")
        for i in badFiles:
            print(i)
