# imports
from C2_ImportHelpers import *
from GenGetters import *

dir = ("C:/Users/LuciusFish/Desktop/motoFiles/")
cats = getCats()
for cat in cats:
    if "FP" in cat:
        cats.remove(cat)
cats.append("FP")
yrs = getYrs()

finFiles = getFinFiles()

print(cats)
print(yrs)
print(finFiles)


# for yr in yrs:
#     for cat in cats:
#         filter_files = fnmatch.filter(listdir(dir)), f"{yr}*{cat}.csv"
#         fileList = [f"{dir}/{file}" for file in filter_files]
#         for file in filelist:
#             if file not in finFiles:
#                 with open(file, r) as csvFile:
#                     csvReader = csv.reader(csvFile, delimiter = ",")
#                     importFlag = testReader(csvReader)
#                     if importFlag == True:








