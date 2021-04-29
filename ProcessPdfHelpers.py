# imports
from os import listdir
import fnmatch


# 1) Get File Helpers
def getRaceFiles(yr, dir):
    rcFiles = fnmatch.filter(listdir(dir), f"{yr}*RAC*nalysis.pdf")
    new_files = [f"{dir}/{file}" for file in rcFiles]
    return new_files

# 2) Parse File Helpers

