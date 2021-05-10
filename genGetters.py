def getImportFinFiles():
    finFiles = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/importFinFiles.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            finFiles.append(i)

    for i in finFiles:
        if i == 0 or i == []:
            del i

    return finFiles

def getCsvFinFiles():
    finFiles = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/csvFinFiles.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            finFiles.append(i)

    for i in finFiles:
        if i == 0 or i == []:
            del i

    return finFiles

def getLeagues():
    lges = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/leagues.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            lges.append(i)

    for i in lges:
        if i == 0 or i == []:
            del i

    return lges

def getYrs():
    yrs = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/years.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            yrs.append(i)

    for i in yrs:
        if i == 0 or i == []:
            del i

    return yrs

def getNations():
    nations = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/nations.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            nations.append(i)

    for i in nations:
        if i == 0 or i == []:
            del i

    return nations

def getManufacturers():
    manufacturers = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/years.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            manufacturers.append(i)

    for i in manufacturers:
        if i == 0 or i == []:
            del i

    return manufacturers

def getCats():
    cats = []
    with open("C:/Users/LuciusFish/Desktop/MotoFiles/cats.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            cats.append(i)

    for i in cats:
        if i == 0 or i == []:
            del i

    return cats

