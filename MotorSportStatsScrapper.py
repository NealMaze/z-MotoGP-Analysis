""" Possible Sources
* https://results.motorsportstats.com/series/motogp/season/2020 *
https://www.thesportsdb.com/league/4407
"""

# import modules
import requests
import os
from bs4 import BeautifulSoup
import time
from collections import defaultdict
from pprint import pprint
import numpy as np
import pandas as pd
from SoupCleaners import *

urlBase = "https://results.motorsportstats.com/series/motogp/season/"

years = ["2019"]

def getSoup(url):
    """ Returns a BeautifulSoup object for the provided url """
    # send get request to url and stores it in htmlReturn
    htmlReturn = requests.get(url)
    # transforms htmlReturn into text object
    textReturn = htmlReturn.text
    # uses html.parser to turn the text object into a beautifulSoup object
    soup = BeautifulSoup(textReturn, "html.parser")
    # returns the soup variable
    return soup

""" Get"""

def getAllRaces(soup):
def getEventInfo(race):
def getRider(race):

for year in years:
    soup = getSoup(url + year)