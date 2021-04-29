"""
example URLs
baseUrl = https://www.motogp.com/en/Results+Statistics/
url_yr = https://www.motogp.com/en/Results+Statistics/2020
url_rc = https://www.motogp.com/en/Results+Statistics/2020/QAT/
url_c = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/
url_ssn = https://www.motogp.com/en/Results+Statistics/2020/QAT/Moto2/FP1/Classification
"""

# import necessary modules
from pdfHelpers import *

# in-depth analysis is only available as far back as 1998
years = ["2021", "2020", "2019", "2018", "2017", '2016', '2015', "2014", '2013', '2012', '2011', '2010', '2009',
          '2008', '2007', '2006', '2005', "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

yearsF = []

base_url = 'http://www.motogp.com/en/Results+Statistics/'

for yr in years:
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

        for cat in categories:
            CAT = cat.text
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


