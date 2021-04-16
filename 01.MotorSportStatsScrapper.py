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
RoundClassUrl = "https://results.motorsportstats.com/results/2020-gran-premio-red-bull-de-espana-2/classification"
RoundFactUrl = "https://results.motorsportstats.com/results/2020-gran-premio-red-bull-de-espana-2/session-facts"
sessionTimesUrl = "https://results.motorsportstats.com/results/2020-gran-premio-red-bull-de-espana-2/session-facts/427fa170-1f81-46cf-b28f-59a790cd605c?fact=LapTime"

##############################################################################################
# getTables(url)
##############################################################################################

def getSessionTables(url):

    ### NEED TO LEARN/ADD Selenium here to activate the tables in the page before retrieving
        # the HTML.

    soup = getSoup(url)


    # sessionUrls = []
    # hrefList = []
    # actTags = []
    # sessionData = soup.find_all('div', class_="_1CDKX")
    # baseUrl = "https://results.motorsportstats.com"
    # urlEnd = "?fact=LapTime"
    #
    # for session in sessionData:
    #     aTags = session.find_all("a")
    #     for tag in aTags:
    #         hrefTag = tag["href"]
    #         if "session-facts/" in hrefTag and hrefTag not in hrefList:
    #             actTags.append(tag.text)
    #             hrefList.append(hrefTag)
    #             fullUrl = baseUrl + hrefTag + urlEnd
    #             sessionUrls.append(fullUrl)
    # return sessionUrls, actTags

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
































