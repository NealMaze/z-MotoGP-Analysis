""" Possible Sources
* https://results.motorsportstats.com/series/motogp/season/2020 *
https://github.com/Vishwacorp/motogp_regression/blob/master/MotoGP_01_results_scraping.ipynb
https://www.thesportsdb.com/league/4407

"""

# import modules
from ScrapperHelpers import *
import os
import time
from collections import defaultdict
from pprint import pprint
import numpy as np
import pandas as pd
########################################################################################################################

seasonUrl = "https://results.motorsportstats.com/series/motogp/season/2020"
raceClassUrl = "https://results.motorsportstats.com/results/2020-gran-premio-red-bull-de-espana-2/classification"
raceFactUrl = "https://results.motorsportstats.com/results/2020-gran-premio-red-bull-de-espana-2/session-facts"

########################################################################################################################
# getSessionUrls(url)
########################################################################################################################

def getSessionUrls(url):
    soup = getSoup(url)
    sessionUrls = []
    sessionData = soup.find_all('div', class_="_1CDKX")
    baseUrl = "https://results.motorsportstats.com"

    for session in sessionData:
        aTags = session.find_all("a")
        for tag in aTags:
            hrefTag = tag["href"]
        if hasattr(session.a, "text") and "results" # STOPPED HERE



sessions = getSessionUrls(raceFactUrl)
for session in sessions:
    print(session)

##############################################################################################
# getTableData(url)
##############################################################################################


##############################################################################################
#
##############################################################################################


##############################################################################################
#
##############################################################################################


##############################################################################################
#
##############################################################################################


##############################################################################################
#
##############################################################################################
