# imports
from B2_ConverterHelpers import *

yrs = ["2021", "2020", "2019", "2018", "2017", "2016", "2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008",
       "2007", "2006", "2005", "2004", "2003", "2002"]
# lges = ["Moto3"]
# rnd = "8"

now = datetime.now()
startTime = now.strftime("%H:%M:%S")
badFiles = []
print("B1_PdfToCsvConverter.py")

for yr in yrs:
    for lge in lges:
        rcFiles = getFiles(pdfDir, f"{yr}*Round_{rnd}-*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print("")
            cur = datetime.now()
            curTime = cur.strftime("%H:%M:%S")
            print(f"   start time = {startTime}")
            print(f" current time = {curTime}")
            print(f"    - - - {yr} {lge} - - - ")

        for file in rcFiles:
            fileName = file.replace(pdfDir, "")
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

            const = ["const", month, day, yr, lge, round, sesType, track,]
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

            headers = ["index", "month", "day", "yr", "lge", "rnd", "session", "trk",
                       "pos", "rdr_num", "f_name", "l_name", "nat", "team", "manu", "num_of_laps",
                       "run_num", "f_tire", "r_tire", "laps_on_f", "laps_on_r", "lap_num", "lap_time", "lap_seconds",
                       "lap_val", "pit", "sec_one", "one_seconds", "one_val", "sec_two", "two_seconds", "two_val",
                       "sec_thr", "thr_seconds", "thr_val", "sec_four", "four_seconds", "four_val", "avg_spd"]
            saveCSV(secMat, saveName, headers)
            # frequency = 500
            # duration = 300
            # Beep(frequency, duration)
            #
            # csvFinFiles.append(file)
            # with open(f"{sveDir}csvFinFiles.txt", "w") as f:
            #     for i in csvFinFiles:
            #         f.write(i + "\\n")

            del rows
            del cRows
            del matrix
            # except:
            #     print(f"\nFailed Parsing:\n{fileName}\n")
            #     badFiles.append(fileName)

end = datetime.now()
endTime = end.strftime("%H:%M:%S")
print("\nparsing finished")
print(f"start time = {startTime}")
print(f"end time = {endTime}")
print("\nFailed Files: ")
for i in badFiles:
    print(i)
