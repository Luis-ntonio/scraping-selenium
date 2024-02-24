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
full_model = {}
urlss = []
def main():
    i = 0
    with open('./data/mobiles/urls/final_urls.json') as f:
        urls = json.load(f)
    for url in urls:
        driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
        
        try:
            driver.get(url)
            time.sleep(1)
            full_spec = {}

            specs = driver.find_element(by=By.ID, value="specificationsTab")
            specs = specs.find_elements(by=By.CLASS_NAME, value="stack-inline")
            launch_day = specs[0].find_element(by=By.CLASS_NAME, value="col-12")
            full_spec["Launch Date"] = launch_day.text
            sub_specs = specs[0].find_elements(by=By.CLASS_NAME, value="col-6")
            for sub_spec in sub_specs:
                try:
                    title = sub_spec.find_element(by=By.TAG_NAME, value="span")
                    full_spec[title.text] = {}
                    sub_class = sub_spec.find_elements(by=By.TAG_NAME, value="tbody")
                    sub_class = sub_class[0].find_elements(by=By.TAG_NAME, value="tr")
                    for sub in sub_class:
                        sub_title = sub.find_element(by=By.CLASS_NAME, value="txt-clr-jumbo")
                        content = sub.find_element(by=By.CLASS_NAME, value = "w-60")
                        content = content.text.split('\n')
                        full_spec[title.text][sub_title.text] = content
                except:
                    pass
            full_model[url] = full_spec
            driver.close()
            driver.quit()
        except:
            urlss.append(url)
        i += 1
        print(i)
    
    with open('./data/mobiles/mainpage/fullspecs.json', 'w', encoding='UTF-8') as f:
        json.dump(full_model, f, indent=4, ensure_ascii=False)
    with open('./data/mobiles/urls/urls_fullspecs_err.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, indent=4, ensure_ascii=False)
main()