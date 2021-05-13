# imports
import fnmatch
from os import listdir, mkdir

saveDir = "C:/Users/LuciusFish/Desktop/motoFiles/listFiles/"

def getImportFinFiles():
    finFiles = []
    with open(f"{saveDir}importFinFiles.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            finFiles.append(i)

    for i in finFiles:
        if i == 0 or i == []:
            del i

    return finFiles

def getCsvFinFiles():
    finFiles = []
    with open(f"{saveDir}csvFinFiles.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            finFiles.append(i)

    for i in finFiles:
        if i == 0 or i == []:
            del i

    return finFiles

def getListFile(type):
    xs = []
    k = []
    with open(f"{saveDir}{type}.txt", "r") as f:
        contents = f.readlines()
        for i in contents:
            xs.append(i.strip().split("\t"))

    for i in xs:
        if i == 0 or i == []:
            del i

    for i in xs:
        for j in i:
            k.append(j)

    return k

def getMatchFiles(dir, string):
    """Searches the directory for appropriate files and creates a list to cycle through"""

    filter_files = fnmatch.filter(listdir(dir), string)
    appFiles = [f"{dir}/{file}" for file in filter_files]

    return appFiles