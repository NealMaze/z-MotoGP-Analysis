# import necessary modules
from A2_ScrappingHelpers import *
from B2_ConverterHelpers import *

def getRoundFiles(yr, rn, fileNum):
    eventWeather = []
    with open(f"{csvWeatherDir}{yr}_EventWeather.csv", "r", encoding = "utf8") as werkFile:
        i = csv.reader(werkFile, delimiter=",")
        for r in i:
            eventWeather.append(r)

    seasonRiders = []
    with open(f"{csvRidersDir}{yr}_Riders.csv", "r", encoding = "utf8") as workFile:
        i = csv.reader(workFile, delimiter=",")
        for r in i:
            seasonRiders.append(r)

    try:
        eventWeather.pop(0)
    except:
        eventWeather = []

    try:
        seasonRiders.pop(0)
    except:
        seasonRiders = []

    base_url = 'http://www.motogp.com/en/Results+Statistics/'
    dest = "C:/Users/LuciusFish/Desktop/motoFiles/"
    time.sleep(0 + np.random.random())
    TRK = rn['value']
    Track = rn['title']
    urlWk = base_url + yr + '/' + TRK + '/'
    soupWk = soup_special(urlWk)
    categories = get_all_cats(soupWk)
    print(f"{yr} Round: {fileNum}")

    for cat in categories:
        time.sleep(0 + np.random.random())
        CAT = cat.text
        url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
        soup_c = soup_special(url_c)
        sessions = get_all_sessions(soup_c)
        print(f"{CAT}")

        for ssn in sessions:
            time.sleep(0 + np.random.random())
            SSN = ssn
            if ssn == "RACE":
                SSN = "RAC"
            if ssn == "RACE2":
                SSN = "RAC2"
            url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
            soupSSN = soup_special(url_ssn)
            pdfLinks = getPDFs(soupSSN)
            x = f"{SSN}, "

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
                fName = f"{dest}pdfFiles/{yr}-Round_{fileNum}-{CAT}-{Track}-{ssn}_{v}"
                with open(f"{fName}.pdf", "wb") as f:
                    f.write(pdf.content)
                    x = x + f"{v}, "
            print(x)

    wHeader = ["Year", "Date", "Track", "League", "Session_Type", "Track_Conditions", "Track_Temp", "Air_Temp", "Humidity"]
    yName = f"{dest}csvFiles/weather/{yr}_EventWeather.csv"
    saveCSV(eventWeather, yName, wHeader)

    rHeader = ["Year", "League", "Number", "Name", "Nation", "Team", "Bike"]
    rName = f"{dest}csvFiles/riders/{yr}_Riders.csv"
    saveCSV(seasonRiders, rName, rHeader)

def getFiles(yr):
    # if yr == "all":
    #     yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009",
    #            "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]
    #     base_url = 'http://www.motogp.com/en/Results+Statistics/'
    #     dest = "C:/Users/LuciusFish/Desktop/motoFiles/"
    #
    #     for yr in yrs:
    #         time.sleep(0 + np.random.random())
    #         eventWeather = []
    #         seasonRiders = []
    #
    #         fileNum = 0
    #         url_yr = base_url + yr
    #         soupYr = soup_special(url_yr)
    #         rounds = getAllRounds(soupYr)
    #
    #         for rn in rounds:
    #             fileNum += 1
    #             getRoundFiles(rn, fileNum)
    #
    #         print("")

    # else:
    #     base_url = 'http://www.motogp.com/en/Results+Statistics/'
    #     dest = "C:/Users/LuciusFish/Desktop/motoFiles/"
    #     url_yr = base_url + yr
    #     soupYr = soup_special(url_yr)
    #     rounds = getAllRounds(soupYr)
    rndIn = input("retrieve files from round: ")
    #     print("")
    #     rndReq = int(rndIn)
    #     rnIndx = rndReq - 1
    #     rn = rounds[rnIndx]
    #     getRoundFiles(yr, rn, rndReq)

def convertYrPdfs(yr):
    now = datetime.now()
    startTime = now.strftime("%H:%M:%S")
    badFiles = []

    for lge in lges:
        rcFiles = getFiles(f"{pdfDir}{yr}*Round_*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print("")
            cur = datetime.now()
            curTime = cur.strftime("%H:%M:%S")
            print(f"   start time = {startTime}")
            print(f" current time = {curTime}")
            print(f"    - - - {yr} {lge} - - - ")

        for file in rcFiles:
            fileName = file.replace(pdfDir, "")
            try:
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
                    else:
                        print("line 228")
                        exit()

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

            except:
                print(f"\nFailed Parsing:\n{fileName}\n")
                badFiles.append(fileName)

    end = datetime.now()
    endTime = end.strftime("%H:%M:%S")
    print("\nparsing finished")
    print(f"start time = {startTime}")
    print(f"end time = {endTime}")
    print("\nFailed Files: ")
    for i in badFiles:
        print(i)

