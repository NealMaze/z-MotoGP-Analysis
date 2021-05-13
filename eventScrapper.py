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
categories = getListFile("cats")

base_url = 'http://www.motogp.com/en/Results+Statistics/'

for yr in yrs:
    fileNum = 1
    url_yr = base_url + yr
    soupYr = soup_special(url_yr)
    round = getAllRounds(soupYr)
    print(f"\n{yr}")

    for rn in round:
        TRK = rn['value']
        Track = rn['title']
        urlWk = base_url + yr + '/' + TRK + '/'
        soupWk = soup_special(urlWk)
        categories = get_all_cats(soupWk)

        for cat in categories:
            CAT = cat.text
            url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
            soup_c = soup_special(url_c)
            sessions = get_all_sessions(soup_c)

            for ssn in sessions:
                SSN = ssn
                if ssn == "RACE":
                    SSN = "RAC"
                if ssn == "RACE2":
                    SSN = "RAC2"
                url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
                soupSSN = soup_special(url_ssn)

                weather, riders = getAllStats(soup_ssn, yr, TRK, Track, CAT, SSN)

                time.sleep(30 + np.random.random())

            exit()


        fileNum += 1

print('>> Scraping complete!')
