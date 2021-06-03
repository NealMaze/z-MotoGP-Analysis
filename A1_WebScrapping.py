"""
example URLs
baseUrl = https://www.motogp.com/en/Results+Statistics/
url_yr = https://www.motogp.com/en/Results+Statistics/2020
url_rc = https://www.motogp.com/en/Results+Statistics/2020/QAT/
url_c = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/
url_ssn = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/FP1/Classification
"""

# import necessary modules
from A2_ScrappingHelpers import *
from GenGetters import *

# in-depth analysis is only available as far back as 1998
yrs = getListFile("yrs")
yrs = ["2009", "2008", "2007", "2006", "2005", "2004", "2003", "2002", "2001", "2000",
       "1999", "1998"]

base_url = 'http://www.motogp.com/en/Results+Statistics/'

dest = "C:/Users/LuciusFish/Desktop/motoFiles/"

# for yr in yrs:
#     time.sleep(0 + np.random.random())
#     eventWeather = []
#     seasonRiders = []
#
#     fileNum = 1
#     url_yr = base_url + yr
#     soupYr = soup_special(url_yr)
#     rounds = getAllRounds(soupYr)
#     print(f"\n")
#
#     for rn in rounds:
#         time.sleep(0 + np.random.random())
#         TRK = rn['value']
#         Track = rn['title']
#         urlWk = base_url + yr + '/' + TRK + '/'
#         soupWk = soup_special(urlWk)
#         categories = get_all_cats(soupWk)
#         print(f"{yr} Round: {fileNum}")
#
#         for cat in categories:
#             time.sleep(0 + np.random.random())
#             CAT = cat.text
#             url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
#             soup_c = soup_special(url_c)
#             sessions = get_all_sessions(soup_c)
#             print(f"{CAT}")
#
#             for ssn in sessions:
#                 time.sleep(0 + np.random.random())
#                 SSN = ssn
#                 if ssn == "RACE":
#                     SSN = "RAC"
#                 if ssn == "RACE2":
#                     SSN = "RAC2"
#                 url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
#                 soupSSN = soup_special(url_ssn)
#                 pdfLinks = getPDFs(soupSSN)
#                 x = f"{SSN}, "
#
#                 weather, riders = getAllStats(soupSSN, yr, TRK, Track, CAT, SSN)
#                 eventWeather.append(weather)
#                 for rider in riders:
#                     if rider not in seasonRiders:
#                         seasonRiders.append(rider)
#
#                 for link in pdfLinks:
#                     time.sleep(1 + np.random.random())
#                     t = link.split("/")
#                     u = t[9].split(".")
#                     v = u[0]
#                     pdf = requests.get(link)
#                     fName = f"{dest}moto_pdf/{yr}-Round_{fileNum}-{CAT}-{Track}-{ssn}_{v}"
#                     with open(f"{fName}.pdf", "wb") as f:
#                         f.write(pdf.content)
#                         x = x + f"{v}, "
#
#                 print(x)
#
#         fileNum += 1
#
#     heads = ["Year", "Date", "Track", "League", "Session_Type", "Track_Conditions", "Track_Temp", "Air_Temp", "Humidity"]
#     yName = f"{dest}moto_csv/{yr}_EventWeather.csv"
#     saveCSV(eventWeather, yName)
#
#     rHeader = ["Year", "League", "Number", "Name", "Nation", "Team", "Bike"]
#     rName = f"{dest}moto_csv/{yr}_Riders.csv"
#     saveCSV(seasonRiders, rName)

print('>> Scraping complete!')


