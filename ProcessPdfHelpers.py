# imports
from os import listdir
import pdfplumber as plumb
import fnmatch

# 1) Get File Helpers
def getRacAnalysis(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rc_files = [f"{dir}/{file}" for file in filter_files]
    return rc_files

def getIndex(lis, text):
    index = lis.index(text)
    return index

def getRiderName(lis):
    rid_name = lis[0] + " " + lis[1]
    del lis[0:2]
    return rid_name

def getRiderTeam(lis):
    ## create list of nationalities
    ## while working line != list of nationalities:
    ## append and remove team names
    nations = ["JPN", "ITA", "USA", "AUS", "SPA", "SWI", "NED", "GBR", "MAL", "INA", "THA", "GER", "RSA", "FRA", "POR"]
    team = []
    while lis[0] not in nations:
        team.append(lis[0])
        del lis[0]
    nat = lis[0]
    del lis[0]
    return team, nat

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

def getRiderInfo(lis, pos):
    rid_info = []
    name = getRiderName(lis)
    rid_info.append(name)
    team, nat = getRiderTeam(lis)
    rid_info.append(team)
    rid_info.append(nat)

    x = 0
    while lis[x] != pos:
        x += 1

    lis.remove(lis[x])
    num = lis[x]
    rid_info.insert(0, num)
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])
    str_laps = lis[x]
    lis.remove(lis[x])
    lis.remove(lis[x])
    lis.remove(lis[x])

    laps = str_laps.replace("laps=", "")
    rid_info.insert(0, laps)
    return rid_info

def getTxt(pages):
    text = []
    positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
                 "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
                 "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]
    pos = []
    txts = []
    x = 0

    for pg in pages:
        words = pg.extract_words()
        txt = []
        for i in words:
            txt.append(i["text"])
        txts.append(txt)

    for txt in txts:
        stripBoilerPlate(txt)
        for t in txt:
            if t in positions:
                pos.append(positions[x])
                x += 1
            text.append(t)
        text.append("End_Row")
        text.append("End_Page")

    return text, pos

def stripBoilerPlate(lis):
    x = 0
    while "Speed" not in lis[x]:
        x += 1
    x += 1
    del lis[0:x]
    x = 0
    while "Speed" not in lis[x]:
        x += 1
    x += 1
    del lis[0:x]
    end_index = lis.index("Fastest")
    del lis[end_index:]

def getLaps(lis, const, rider, session):
    x = 1
    y = int(rider[0])
    rider.remove(rider[0])
    for i in rider:
        const.append(i)

    for lap in range(0, y):
        i = 0

        while lis[i] != str(x):
            i += 1
            if lis[0] == "End_Page":
                del lis[0]
                i = 0
            if lis[i] == "End_Page":
                print("hit end of page")
                i = 0

        if lis[i] == str(x):
            lap_data = []
            for l in const:
                lap_data.append(l)
            lap_data.append(x)         # Lap Number
            del lis[i:i+1]
            lap_data.append(lis[i])    # Lap Time
            del lis[i:i+1]
            lap_data.append(lis[i])    # Sec 1 Time
            del lis[i:i+1]
            lap_data.append(lis[i])    # Sec 2 Time
            del lis[i:i+1]
            lap_data.append(lis[i])    # Sec 3 Time
            del lis[i:i+1]
            lap_data.append(lis[i])    # Sec 4 Time
            del lis[i:i+1]
            lap_data.append(lis[i])    # Avg Speed
            del lis[i:i+1]
            session.append(lap_data)
            x += 1
            i += 1
    print(f"Finished {lap_data[6]}'s laps")

def getRider(lis):
    rider = []
    (f"{lis[0]} {lis[1]}")
    del lis[0:2]
    team = 
