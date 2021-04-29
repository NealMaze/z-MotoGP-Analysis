# imports
from pdfHelpers import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


driver = webdriver.Firefox(executable_path = r"..\z-MotoGP-Analysis\geckodriver.exe")

years = ["2021", "2020", "2019", "2018", "2017", '2016', '2015', "2014", '2013', '2012', '2011', '2010', '2009', '2008',
         '2007', '2006', '2005', "2004", "2003", "2002", "2001", "2000", "1999", "1998"]

base_url = 'http://www.motogp.com/en/Results+Statistics/2021'

driver.get(base_url)
seasonKnob = driver.find_element_by_id("handle_season")

for yr in years:
    testNo = 1
    selectedYear = driver.find_element_by_id("selected_season").text
    if selectedYear != yr:
        while selectedYear > yr:
            seasonKnob.send_keys(Keys.ARROW_LEFT)
            selectedYear = driver.find_element_by_id("selected_season").text
            driver.implicitly_wait(2)
        while selectedYear < yr:
            seasonKnob.send_keys(Keys.ARROW_RIGHT)
            selectedYear = driver.find_element_by_id("selected_season").text
            driver.implicitly_wait(2)
    offSeasonTests = driver.find_elements_by_link_text("Results")
    links = [test.get_attribute("href") for test in offSeasonTests]
    print(f"\n {yr}")
    for link in links:
        print(link)
        soupTest = soup_special(link)
        find = soupTest.find_all(class_ = "pdf", )
        if find is None:
            print(f"{yr} no tests found")
        else:
            for i in find:
                if "analysis" in i["title"]:
                    x = i["href"]
                    pdf = requests.get(x)
                    fname = f"{yr}Test{testNo}"
                    print(f" - - - - - - {fname}")
                    with open(f"{fname}.pdf", "wb") as f:
                        f.write(pdf.content)
                    testNo += 1












