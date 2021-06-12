# imports
from B2_ConverterHelpers import *

yrs = ["2015", "2014", "2013", "2012", "2011", "2010", "2009", "2008",
       "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]
# lges = ["Moto3"]
# rnd = "1"

now = datetime.now()
startTime = now.strftime("%H:%M:%S")
print("B1_PdfToCsvConverter.py")

for yr in yrs:
    for lge in lges:
        rcFiles = getFiles(pdfDir, f"{yr}*Round_{rnd}-*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in rcFiles:

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

            const = ["const",month, day, yr, lge, round, sesType, track,]
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
            mat = matFormat(matrix)
            headers = ["month", "day", "yr", "lge", "rnd", "session", "trk",
                       "pos", "rdr_num", "f_name", "l_name", "nat", "team", "manu", "num_of_laps",
                       "run_num", "f_tire", "r_tire", "laps_on_f", "laps_on_r",
                       "lap_num", "lap_time", "pit", "sec_one", "sec_two", "sec_thr", "sec_four",
                       "sec_fiv", "sec_six", "sec_sev", "sec_eig", "avg_spd"]
            saveCSV(mat, saveName, headers)
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

end = datetime.now()
endTime = now.strftime("%H:%M:%S")
print(f"start time = {startTime}")
print(f"end time = {endTime}")