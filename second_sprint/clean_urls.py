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

urlss = []
urlss_err = []
def main():
    i = 0
    with open('./data/mobiles/urls/urls.json') as f:
        urls = json.load(f)
    for url in urls:
        flg_btn = False
        driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
        
        try:
            driver.get(url)
            time.sleep(1)

            breadcrumb = driver.find_element(by=By.ID, value="product_tabs_menu")
            butn = breadcrumb.find_elements(by=By.CLASS_NAME, value="prdhdr--dsabld-lnk")

            for btn in butn:
                if btn.text == "Quick Review":
                    flg_btn = True
                    break

            if flg_btn == False:
                urlss.append(url)
            driver.close()
            driver.quit()
        except:
            urlss_err.append(url)
        i += 1
        print(i)

    with open('./data/mobiles/urls/final_urls.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, indent=4, ensure_ascii=False)

    with open('./data/mobiles/urls/final_urls_err.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss_err, f, indent=4, ensure_ascii=False)
main()