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
##############################################################################################

raceFactUrl = "https://results.motorsportstats.com/results/2020-gran-premio-red-bull-de-espana-2/session-facts"


#raceClassUrls, raceFactsUrls = getRaceUrls("https://results.motorsportstats.com/series/motogp/season/2020")

# for race in raceFactsUrls:
#     print(race)


