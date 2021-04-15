
import requests
from bs4 import BeautifulSoup

##############################################################################################
# getSoup()
##############################################################################################

# maybe make this private so that outside the helpers, you never use a soup object

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

##############################################################################################
# getSeasonRaceUrls()
##############################################################################################

def getSeasonRaceUrls(url):
    soup = getSoup(url)
    raceClassificationUrls = []
    raceFactsUrls = []
    hrefList = []
    racesData = soup.find_all('td', class_="_2sWDi f4AjL")
    baseUrl = "https://results.motorsportstats.com"

    for race in racesData:
        aTags = race.find_all("a")
        for tag in aTags:
            hrefTag = tag["href"]
        if hasattr(race.a, "text") and "results" in hrefTag and hrefTag not in hrefList:
            fullUrl = f"{baseUrl}{hrefTag}"
            raceClassificationUrls.append(fullUrl)
            hrefList.append(hrefTag)
    for url in raceClassificationUrls:
        newUrl = url.replace("classification","session-facts")
        raceFactsUrls.append(newUrl)
    return raceClassificationUrls, raceFactsUrls

########################################################################################################################
# getSessionUrls(url)
########################################################################################################################

def getSessionUrls(url):
    soup = getSoup(url)
    sessionUrls = []
    hrefList = []
    actTags = []
    sessionData = soup.find_all('div', class_="_1CDKX")
    baseUrl = "https://results.motorsportstats.com"
    urlEnd = "?fact=LapTime"

    for session in sessionData:
        aTags = session.find_all("a")
        for tag in aTags:
            hrefTag = tag["href"]
            if "session-facts/" in hrefTag and hrefTag not in hrefList:
                actTags.append(tag.text)
                hrefList.append(hrefTag)
                fullUrl = baseUrl + hrefTag + urlEnd
                sessionUrls.append(fullUrl)
    return sessionUrls, actTags







##############################################################################################
# getRiders() is depricated
##############################################################################################

def getRiders(soup):
    riders = []
    ridersData = soup.find_all('td', class_="_2sWDi f4AjL")

    for rider in ridersData:
        aTags = rider.find_all("a")
        for tag in aTags:
            hrefTag = tag["href"]
        if hasattr(rider.a, "text") and "drivers" in hrefTag and rider.a.text not in riders:
            riders.append(rider.a.text)
    return riders

##############################################################################################
#
##############################################################################################





