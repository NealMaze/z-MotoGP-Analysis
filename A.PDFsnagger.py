"""
example URLs
baseUrl = https://www.motogp.com/en/Results+Statistics/
url_yr = https://www.motogp.com/en/Results+Statistics/2020
url_rc = https://www.motogp.com/en/Results+Statistics/2020/QAT/
url_c = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/
url_ssn = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/FP1/Classification
"""

# import necessary modules
from A2.pdfHelpers import *
from genGetters import *

# in-depth analysis is only available as far back as 1998
yrs = getYrs()
categories = getCats()

base_url = 'http://www.motogp.com/en/Results+Statistics/'

for yr in yrs:
    fileNum = 1
    url_yr = base_url + yr
    soupYr = soup_special(url_yr)
    round = get_all_races(soupYr)
    print(f"\n{yr}")

    for rn in round:
        TRK = rn['value']
        Track = rn['title']
        urlWk = base_url + yr + '/' + TRK + '/'
        soupWk = soup_special(urlWk)
        categories = get_all_cats(soupWk)

        for cat in categories[:2]:
            CAT = cat.text
            CAT = "RAC2"
            url_c = base_url + yr + '/' + TRK + '/' + CAT + '/'
            soup_c = soup_special(url_c)
            sessions = get_all_sessions(soup_c)
            print(f"{CAT}")

            for ssn in sessions:
                SSN = ssn
                if ssn == "RACE":
                    SSN = "RAC"
                url_ssn = base_url + yr + '/' + TRK + '/' + CAT + '/' + SSN + '/Classification'
                soupSSN = soup_special(url_ssn)
                pdfLinks = getPDFs(soupSSN)
                x = f"{SSN}, "

                for link in pdfLinks:
                    t = link.split("/")
                    u = t[9].split(".")
                    v = u[0]
                    pdf = requests.get(link)
                    fName = f"{yr}-Round_{fileNum}-{CAT}-{TRK}-{ssn}_{v}"
                    with open(f"{fName}.pdf", "wb") as f:
                        f.write(pdf.content)
                        x = x + f"{v}, "

                print(x)
                time.sleep(1 + np.random.random())

        fileNum += 1

print('>> Scraping complete!')


