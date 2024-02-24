import concurrent.futures

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import json
import random


options = webdriver.ChromeOptions()
url = "https://pricebaba.com/search?status=10&status=20&status=30&status=40&from=Mobile+Phones&active=true&sort=online_price-desc&category=MOBILE&start=0&limit=40"

urls = []

def main():
    i = 1
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
    driver.get(url)

    
    pages = driver.find_elements(By.CLASS_NAME, "pgntn-lnks")
    pages = pages[0].find_elements(By.TAG_NAME, "li")
    
    while pages[-1].text == "Next":
        products = driver.find_elements(By.XPATH, "//span[@data-action='kr-ga-track']")
        for product in products:
            link = product.get_attribute("data-href")
            urls.append(link)
        pages[-1].click()
        time.sleep(2)

        pages = driver.find_elements(By.CLASS_NAME, "pgntn-lnks")
        pages = pages[0].find_elements(By.TAG_NAME, "li")
        print(i)
        i += 1
    driver.close()
    driver.quit()

    with open('./data/mobiles/urls/urls.json', 'w', encoding='UTF-8') as f:
        json.dump(urls, f, indent=4, ensure_ascii=False)
main()