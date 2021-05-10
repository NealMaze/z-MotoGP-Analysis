# imports
from C2.importHelpers import *
from genGetters import *

dir = ("C:/Users/LuciusFish/Desktop/motoFiles/")
types = ["RAC", "RAC2", "Q2", "Q1", "WUP", "FP1", "FP2", "FP3", "FP4", "Test"]
yrs = getYrs()

finFiles = getFinFiles()

for yr in yrs:
    for sesType in Types:
        filter_files = fnmatch.filter(listdir(dir)), f"{yr}*.csv"
        fileList = [f"{dir}/{file}" for file in filter_files]
        for file in filelist:
            if file not in finFiles:
                with open(file, r) as csvFile:
                    csvReader = csv.reader(csvFile, delimiter = ",")
                    importFlag = testReader(csvReader)
                    if importFlag == True:








