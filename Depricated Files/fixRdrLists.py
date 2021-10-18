from B2_ConverterHelpers import *

def getRidersData(yr):
    data = []
    dataNue = []
    rows = []
    rem = ["'", "[", "]", '"']

    with open(f"{csvDir}{yr}_Riders.csv", "r", encoding="utf8") as yrFile:
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


rs = []

for yr in yrs[:-5]:
    list = []
    riders = getRidersData(yr)
    for i in riders:
        if len(i) not in rs:
            rs.append(len(i))
    print(yr)

    headers = ["Year", "League", "Number", "Name", "Nation", "Team", "Bike"]
    df = pd.DataFrame(riders)
    df.to_csv(f"{csvDir}{yr}RidersV2.csv", index = False, header = False)