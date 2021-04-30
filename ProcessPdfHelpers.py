# imports
from os import listdir
import pdfplumber as plumb
import fnmatch

# 1) Get File Helpers
def getRacAnalysis(yr, dir):
    filter_files = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    rc_files = [f"{dir}/{file}" for file in filter_files]
    return rc_files

def getTxt(pages):
    text = []
    positions = ["1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th", "9th", "10th", "11th", "12th", "13th", "14th",
           "15th", "16th", "17th", "18th", "19th", "20th", "21st", "22nd", "23rd", "24th", "25th", "26th", "27th",
           "28th", "29th", "30th", "31st", "32nd", "33rd", "34th", "35th", "36th", "37th", "38th", "39th", "40th"]
    pos = []
    txts = []

    for pg in pages:
        words = pg.extract_words()
        txt = []
        for i in words:
            txt.append(i["text"])
            if i["text"] in positions:
                pos.append(positions[0])
                positions.remove(positions[0])
        txts.append(txt)

    for txt in txts:
        x = 0
        for t in txt[0:55]:
            print(f"{x}   {t}")
            x +=1
        print("\n")
        # stripBoilerPlate(txt)
        # text.append("End_Page")

    return text, pos

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

def stripBoilerPlate(lis):
    start = lis.index("Lap")
    del lis[0:start]

    # for i in lis[0:]:
    #     x = 1
    #     if "Speed" in i:
    #         del lis[0:x]



    # try:
    #     start = lis.index("Speed") + 1
    #     del lis[0:start]
    #     start = lis.index("Speed") + 1
    #     del lis[0:start]
    # except:
    #     start = lis.index("T4Speed") + 1
    #     del lis[0:start]
    #     start = lis.index("T4Speed") + 1
    #     del lis[0:start]


    end_index = lis.index("Fastest")
    del lis[end_index:]

def getRiderInfo(lis, pos):
    x = 0

    rid_info = []
    name = getRiderName(lis)
    rid_info.append(name)
    team, nat = getRiderTeam(lis)
    rid_info.append(team)
    rid_info.append(nat)

    while lis[x] != pos[0]:
        x += 1

    lis.remove(lis[x])
    num = lis[x]["text"]
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

    pos.remove(pos[0])
    return rid_info

def getLaps(lis, const, rider, race):
    x = 1
    y = int(rider[0])
    rider.remove(rider[0])

    for i in rider:
        const.append(i)

    for i in range(x, y):
        x = 0

        while lis[x] != str(x):
            x += 1

        if lis[x] == str(x):
            lap_data = []
            for i in const:
                lap_data.append(i)
            lap_data.append(x)         # Lap Number
            del lis[x:x+1]
            lap_data.append(lis[x])  # Lap Time
            del lis[x:x+1]
            lap_data.append(lis[x])  # Sec1 Time
            del lis[x:x+1]
            lap_data.append(lis[x])  # Sec2 Time
            del lis[x:x+1]
            lap_data.append(lis[x])  # Sec3 Time
            del lis[x:x+1]
            lap_data.append(lis[x])  # Sec4 Time
            del lis[x:x+1]
            lap_data.append(lis[x])  # Lap Avg Speed
            del lis[x:x+1]
            race.append(lap_data)
        x += 1
