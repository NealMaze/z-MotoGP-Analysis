# imports
from B2_ConverterHelpers import *

# csvFinFiles = getFinFiles("csv")

# yrs = ["2005", "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

for yr in yrs:
    for lge in lges:
        rcFiles = getAnalyFiles(pdfDir, f"{yr}*{lge}*nalysis.pdf")

        if len(rcFiles) != 0:
            print("")
            print(f" - - - {yr}, {lge} - - - ")

        for file in rcFiles:
            for i in ses:
                if i in file:
                    sesType = i
            print(f"\n{file}")
            saveName, track = getSaveName(file, sesType)
            col, date = openPDF(file)
            rows = parsePDF(col, yr)
            const = ["const", yr, date, lge, track, sesType]
            rows.insert(0, const)
            for i in rows:
                print(i)

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################


            # matrix = getMatrix(fRows, const)

            saveCSV(rows, saveName)
            frequency = 500
            duration = 300
            Beep(frequency, duration)

            # csvFinFiles.append(file)
            # with open(f"{sveDir}csvFinFiles.txt", "w") as f:
            #     for i in csvFinFiles:
            #         f.write(i + "\\n")

            del rows
            # del matrix

########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################
########################################################################################################################

                    # if re.match("^\d{1,2}(st|nd|rd|th)$", col[0]["text"]) or re.match("^[a-zA-ZàáâäãåąčćęèéêëėįìíîïłńòóôöõøùúûüųūÿýżźñçčšžÀÁÂÄÃÅĄĆČĖĘÈÉÊËÌÍÎÏĮŁŃÒÓÔÖÕØÙÚÛÜŲŪŸÝŻŹÑßÇŒÆČŠŽ∂ð.]+$", line[0]["text"]):
                    #     print("all good")
                    #
                    # else:
                    #     print("##################################################################")
                    #     for i in col[:4]:
                    #         txt = i["text"]
                    #         loq = i["x0"]
                    #         print(f"{txt}       {loq}")
                    #     print("##################################################################")




                    #


