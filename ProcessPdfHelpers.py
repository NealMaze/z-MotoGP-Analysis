# imports
from os import listdir
import fnmatch

# 1) Get File Helpers
def getRacAnalysis(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rc_files = [f"{dir}/{file}" for file in filter_files]
    return rc_files

def getQualAnalysis(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*QP1*nalysis.pdf")
    filter_two = fnmatch.filter(listdir(dir), f"{yr}*QP2*nalysis.pdf")
    filter_three = fnmatch.filter(listdir(dir), f"{yr}*QP3*nalysis.pdf")
    filter_four = fnmatch.filter(listdir(dir), f"{yr}*QP4*nalysis.pdf")
    # todo


# 2) Parse File Helpers



# 3)
def getIndex(lis, text):
    index = lis.index(text)
    return index

def getRiderName(lis):
    rid_name = lis[0] + " " + lis[1]
    del lis[0:2]
    return rid_name

def getRiderNat(lis):###################################################################################################
########################################################################################################################
    ## create list of nationalities
    ## while working line != list of nationalities:
    ## append and remove team names
########################################################################################################################
########################################################################################################################
    while lis[0]
    nat = lis[0]
    lis.remove(lis[0])
    return nat

def getSessionConstants(pages):
    words = pages[0].extract_words()
    sess_const = []

    year = words[-5]["text"]
    day = words[-6]["text"]
    month = words[-7]["text"]

    date = f"{month} {day} {year}"
    sess_const.append(date)
    sess_const.append(year)
    TRK = words[9]["text"]
    sess_const.append(TRK)
    league = words[8]["text"]
    sess_const.append(league)
    session = words[14]["text"]
    sess_const.append(session)
    return sess_const

def stripBoilerPlate(lis):
    start_index = getIndex(lis, "Speed")
    del lis[0:start_index]
    end_index = getIndex(lis, "Fastest")
    del lis[end_index:]

def getRiderInfo(lis, pos):
    x = 0

    rid_info = []
    rid_info.append(getRiderName(lis))
    rid_info.append(getTeamName(lis))
    rid_info.append(getRiderNat(lis))

    while lis[x]["text"] != pos[0]:
        x += 1

    lis.remove(lis[x])
    num = lis[x]["text"]
    rid_info.insert(0, num)
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])
    str_laps = lis[x]["text"]
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])

    laps = str_laps.replace("laps=", "")
    rid_info.insert(0, laps)

    pos.remove(pos[0])
    return rid_info

def getLaps(lis, const, rider, race):
    x = 1
    y = int(rider[0])
    rider.remove(rider[0])

    for i in rider:
        const.append(i)

    for i in range(x, y):
        lin = 9

        while lis[lin]["text"] != str(x):
            lin += 1

        if lis[lin]["text"] == str(x):
            lap_data = []
            for i in const:
                lap_data.append(i)
            lap_data.append(x)                 # Lap Number
            del lis[lin:lin+1]
            lap_data.append(lis[lin]["text"])  # Lap Time
            del lis[lin:lin+1]
            lap_data.append(lis[lin]["text"])  # Sec1 Time
            del lis[lin:lin+1]
            lap_data.append(lis[lin]["text"])  # Sec2 Time
            del lis[lin:lin+1]
            lap_data.append(lis[lin]["text"])  # Sec3 Time
            del lis[lin:lin+1]
            lap_data.append(lis[lin]["text"])  # Sec4 Time
            del lis[lin:lin+1]
            lap_data.append(lis[lin]["text"])  # Lap Avg Speed
            del lis[lin:lin+1]
            race.append(lap_data)
        x += 1
