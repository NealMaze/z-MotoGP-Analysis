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
from lists import *
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

yr = 2021

# in-depth analysis is only available as far back as 1998

gLnks = []

url = 'http://www.motogp.com/en/Results+Statistics/'
driver = webdriver.Firefox(executable_path = "C:/Users/LuciusFish/Desktop/Bootcamp/z-MotoGP-Analysis/geckodriver.exe")
driver.get(url)

WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.ID, "handle_season")))
knob = driver.find_element_by_id("handle_season")
knob.send_keys(Keys.ARROW_RIGHT)
knob.send_keys(Keys.ARROW_RIGHT)
knob.send_keys(Keys.ARROW_RIGHT)
yr = 2021
count = 50

while yr != 1997:
    print(str(yr))

    count = count + 1
    c = 0
    while c != count:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.TAG_NAME, "a")))
        c = c + 1

    time.sleep(5)

    for i in driver.find_elements_by_xpath(".//a"):
        x = i.get_attribute("href")
        if "TestResults" in x:
            print(x)
            gLnks.append(x)

    knob.send_keys(Keys.ARROW_LEFT)

    yr -= 1

driver.quit()

for link in gLnks:
    pdfs = soup_special(link)
    time.sleep(0 + np.random.random())
    r = pdfs.find_all(href=True)

    time.sleep(1 + np.random.random())


for

# for yr in yrs:
#     fileNum = 1
#     url_yr = base_url + yr
#     soupYr = soup_special(url_yr)
#     round = getAllRounds(soupYr)
#     print(f"\n{yr}")
#
#     for rn in round:
#         TRK = rn['value']
#         Track = rn['title']
#         urlWk = base_url + yr + '/' + TRK + '/'
#         soupWk = soup_special(urlWk)
#         categories = get_all_cats(soupWk)
#
#         for cat in categories:
#             CAT = cat.text
#             url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
#             soup_c = soup_special(url_c)
#             sessions = get_all_sessions(soup_c)
#
#             for ssn in sessions:
#                 SSN = ssn
#                 if ssn == "RACE":
#                     SSN = "RAC"
#                 if ssn == "RACE2":
#                     SSN = "RAC2"
#                 url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
#                 soupSSN = soup_special(url_ssn)
#
#                 weather, riders = getAllStats(soup_ssn, yr, TRK, Track, CAT, SSN)
#
#                 time.sleep(30 + np.random.random())
#
#             exit()
#
#
#         fileNum += 1

print('>> Scraping complete!')
