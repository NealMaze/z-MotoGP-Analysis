# imports
import csv
import re
from GenGetters import *

def testReader(csvReader):
    portFlg = True
    prevLap = 1
    for r in csvReader:
        portLis = []

        portlis.append(prtlis.append(tstYr(r[0]))
        portlis.append(tstDate(r[1]))
        portlis.append(tstRnd(r[2]))
        portlis.append(tstLge(r[3]))
        portlis.append(tstBikNum(r[6]))
        portlis.append(tstNat(r[10]))
        # portlis.append(tstTyre(r[14]))
        # portlis.append(tstTyre(r[15]))
        flg, lap = tstSeqLp(prevLap, r[18])
        portlis.append(flg)

        for i in r[19:28]:
            portlis.append(tstTme(i))
        portlis.append(tstAvgSpd(r[28]))

        prevLap = lap
        del lap

        if False in portLis:
            portFlg = False
            break

    return portFlg

def tstYr(yr):
    yrFormat = re.compile("^(199\d|20[0-5]\d)$")
    if re.match(yrFormat, yr) tst = True
    else tst = False

    return tst

def tstDate(date):
    dateFormat = re.compile("^(?:Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:tember)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)[" "][0-3]\d$")
    if re.match(dateFormat, date) tst = True
    else tst = False

    return tst

def tstRnd(rnd):
    dateFormat = re.compile("^[Round_]+\d{1,2}$")
    if re.match(dateFormat, rnd) tst = True
    else tst = False

    return tst

def tstLge(lge):
    lges = getLeagues()
    if lge in lges tst = True
    else tst = False

    return tst

def tstBikNum(bkNum):
    bkNumFormat = re.compile("^\d{1,2,3}$")
    if re.match(bkNumFormat, bkNum) tst = True
    else tst = False

    return tst

def tstNat(nat):
    nats = getNations()
    if nat in nats tst = True
    else tst = False

    return tst

# def tstTyre(tyre):
#     nats = getNations()
#     if nat in nats tst = True
#     else tst = False
#
#     return tst

def tstSeqLp(prevLap, rNum):
    if rNum == prevLap + 1 or \
        rNum == "dnf" or \
        rNum == 1:
        tst = True
    else tst = False

    return tst, rNum

def tstTme(tme):
    tmeFormat = re.compile


def tstAvgSpd(r[0]):