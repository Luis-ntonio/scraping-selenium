import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

options = webdriver.ChromeOptions()

urls_hindi = []
urls_tamil = []

with open('./data/mobiles/urls/urls.json') as f:
    urls = json.load(f)

for url in urls:
    try:
        driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
        splited = url.split('m/')
        tamil = splited[0] + 'm/ta/' + splited[1]
        hindi = splited[0] + 'm/hi/' + splited[1]
        print(tamil)
        driver.get(tamil)
        flg_err = len(driver.find_elements(By.CLASS_NAME, "err_msg")) > 0
        print(flg_err)
        if flg_err:
             raise Exception('page not found')
        print('adding tamil')
        urls_tamil.append(tamil)
        urls_hindi.append(hindi)
        driver.close()
        driver.quit()

    except Exception as e:
        print(f"{url} has no other language availability")
        driver.close()
        driver.quit()

with open('./data_indi/tablets/urls/urls.json', "w", encoding='utf-8') as f:
        json.dump(urls_hindi, f, indent=4, ensure_ascii=False)

with open('./data_tamil/tablets/urls/urls.json', "w", encoding='utf-8') as f:
        json.dump(urls_tamil, f, indent=4, ensure_ascii=False)