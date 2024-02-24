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
key_model = {}
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
            key_spec = {}

            keys = driver.find_element(by=By.CLASS_NAME, value="keyspec")
            keys = keys.find_elements(by=By.CLASS_NAME, value="p-b-m")
            for key in keys:
                key_name = key.find_element(by=By.TAG_NAME, value="span")
                key_char = key.find_elements(by=By.TAG_NAME, value="li")

                key_spec[key_name.text] = []
                for char in key_char:
                    key_spec[key_name.text].append(char.text)

            key_model[url] = key_spec
            driver.close()
            driver.quit()
        except:
            urlss.append(url)
        
        i += 1
        print(i)
    
    with open('./data/mobiles/mainpage/keys.json', 'w', encoding='UTF-8') as f:
        json.dump(key_model, f, indent=4, ensure_ascii=False)
    with open('./data/mobiles/urls/urls_keys_err.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, indent=4, ensure_ascii=False)
main()