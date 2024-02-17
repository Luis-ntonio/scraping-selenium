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
err={}


options = webdriver.ChromeOptions()
url = "https://gsm.cool/"

model_reviews = {}

# Simulate human typing speed
def type_text(element, text):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))  #

def main():
        with open('data/mobiles/fullspecs/models_fixed.json') as f:
            models = json.load(f)
        for model in models:
            try:
                driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
                driver.get(url)
                boxs = driver.find_elements(by=By.CLASS_NAME, value="page-h")
                search_box = boxs[0].find_element(by=By.CSS_SELECTOR, value="input[type='search']")
                type_text(search_box, model)

                search_box.click()

                time.sleep(1.5)
                items = driver.find_elements(by=By.CLASS_NAME, value="easy-autocomplete-container")
                items = items[0].find_elements(by=By.TAG_NAME, value="li") 
                item = items[0]
                item.click()

                time.sleep(1)

                model_ = driver.find_element(by=By.CLASS_NAME, value="h1-box")
                info = driver.find_elements(by=By.CLASS_NAME, value="info")

                for i in info:
                    review = i.find_elements(by=By.CSS_SELECTOR, value="h2")
                    if len(review) > 0:
                        if review[0].text == "Review":
                            model_reviews[model] = {}
                            model_reviews[model]['model'] = model_.text
                            model_reviews[model]['review'] = i.text
                            break
                        
                driver.quit()
            except Exception as e:
                err[model] = {}
        return 0

main()
print(model_reviews)
with open('data/mobiles/fullspecs/model_reviews.json', 'w', encoding='UTF-8') as f:
    json.dump(model_reviews, f)
with open('data/mobiles/fullspecs/err.json', 'w', encoding='UTF-8') as f:
    json.dump(err, f)