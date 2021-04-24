# import modules
import requests
import os
from bs4 import BeautifulSoup
import time
from collections import defaultdict
from pprint import pprint
import numpy as np
import pandas as pd
from BranchedSoupCleaners import *

# Temporary Variables
yr = "2017"

# Missing Data:
    # look for tires chosen
    # look for data on every individual lap (including track conditions per lap?)

#Possible Problems:
    # check if average speed is accurate accounting for crashes

# Headers for all scraped data
headers = ["Year", "TRK", "Track", "Category", "Session", "Date", "Track_Condition", "Track_Temp", "Air_Temp",
           "Humidity", "Position", "Points", "Rider_Number", "Rider_Name", "Nationality", "Team_Name", "Bike",
           "Avg_Speed", "Time"]

years = ["2020"]

# url to scrap
baseUrl = "http://www.motogp.com/en/Results+Statistics/"

# 1) function to get soup object
def getSoup(url):
    """ Returns a BeautifulSoup object for the provided url """
    # send get request to url and stores it in htmlReturn
    htmlReturn = requests.get(url)
    textReturn = htmlReturn.text
    soup = BeautifulSoup(textReturn, "html.parser")
    return soup








def getRaceSessions(soup):
    """ Returns all the different race sessions (RACE, RACE2, etc.)
        that took place at a particular track in the provided soup """
    find = soup.find(id='session')
    r = []
    if find is None:
        print("soup = " + str(soup))
        print("r = " + str(r))
        print("find = " + str(find))
        return r
    else:
        r2 = find.find_all('session')
        for s in r2:
            if s.text.find('RACE') > -1:
                r.append(s.text.replace('E',''))
        print("soup = " + str(soup))
        print("r = " + str(r))
        print("find = " + str(find))
        print("r2 = " + str(r2))
        return r








for yr in reversed(years):
    dataList = []
    soupYr = getSoup(baseUrl + yr)
    sessions = getRaceSessions(soupYr)

    for rc in sessions:
        TRK = rc['value']
        Track = rc['title']
        print(TRK, end=", ")
        url_rc = baseUrl + yr + '/' + TRK + '/'
        soup_rc = getSoup(url_rc)
        categories = getAllCats(soup_rc)

        for cat in categories:
            CAT = cat.text
            url_c = baseUrl + yr + '/' + TRK + '/' + CAT + '/'
            soup_c = getSoup(url_c)
            sessions = getRaceSessions(soup_c)

            for ssn in sessions:
                SSN = ssn
                url_ssn = baseUrl + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
                soup_ssn = getSoup(url_ssn)
                time.sleep(1 + np.random.random())

df = pd.DataFrame(dataList, columns=headers)
fn = yr + 'Data.csv'
df.to_csv(fn)
print(fn)
time.sleep(1 + np.random.random())





df = pd.DataFrame(dataList, columns=headers)

df.head()
