import re
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import json
import time

def scrapper_main(paten_number,driver):
    url=f"https://data.epo.org/publication-server/rest/v1.2/patents/{paten_number}/document.xml"
    driver.get(url)

def date_process(date,driver,savedIdentifier):
    print (date)
    url = f"https://data.epo.org/publication-server/rest/v1.2/publication-dates/{date}/patents"
    response= requests.get(url)
    patent_numbers = re.findall(r'>(EP\w+)</a>', response.text)
    
    for patent_number in patent_numbers:
        scrapper_main(patent_number,driver,date)

def dates(driver,savedDate,savedIdentifier):
    response = requests.get("https://data.epo.org/publication-server/rest/v1.2/publication-dates")
    dates = re.findall(r'\d{4}/\d{2}/\d{2}', response.text)
    date_list= [
        date.replace('/', '') 
        for date in dates 
        if date >= '2021/10/01'
    ]
    print(len(date_list))
    check=False
    for date in date_list:
        print(date,type(date))
        if(not check and date==savedDate):
            check=True
        if check:
            date_process(date,driver,savedIdentifier)
def main ():
    service = Service(executable_path="chromedriver.exe")
    driver = webdriver.Chrome(service=service)
    savedDate= '20240731'
    savedIdentifier= 'EP3234277W1B8'
    dates(driver,savedDate,savedIdentifier)
    
if __name__ == "__main__":
    main()