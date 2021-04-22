# 2) functions to clean soup object
def getDate(soup):
    """ Returns the date of the race, or "n/a if information does not exist in the soup """
    find = soup.find(class_ = "padbot5")
    if find is None:
        r = "n/a"
    else:
        r = ",".join(find.text.replace(",", " ").split()[-3:])
    return r

def getTrCon(soup):
    """ Returns the track condition during a race, or "n/a" if information does not exist in the soup"""
    find = soup.find(class_ = "sprite_weather track_condition")
    if find is None:
        r = "n/a"
    else:
        r = find.findNext().text.split()[1]
    return r

def getTrTmp(soup):
    """ Returns the track temperature during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather ground')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[1]
    return r

def getAirTmp(soup):
    """ Returns the air temperature during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather air')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[1]
    return r

def getHumidity(soup):
    """ Returns the track humidity during a race, or 'n/a' if
        information does not exist in the provided soup """
    find = soup.find(class_='sprite_weather humidity')
    if find is None:
        r = 'n/a'
    else:
        r = find.findNext().text.split()[1]
    return r

def getAllRaces(soup):
    """ Returns all the races that took place in a particular season
        for which the soup was passed in """
    find = soup.find(id='event')
    if find is None:
        r = []
    else:
        r = find.find_all('option')
    return r

def getAllCats(soup):
    """ Returns all the different categories (MotoGP, Moto2, etc.)
        that took place at a particular track in the provided soup """
    find = soup.find(id='category')
    if find is None:
        r = []
    else:
        r = find.find_all('option')
    return r