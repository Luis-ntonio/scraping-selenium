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
review_dict = {}
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
            review_char = {
                "text": {},
                "Pros": [],
                "Cons": []
            }
            flg_txt = False
            reviews = driver.find_element(by=By.ID, value="quickreview")
            review_block = reviews.find_elements(by=By.CLASS_NAME, value="detail-desc")
            paragraphs = review_block[0].find_elements(by=By.TAG_NAME, value="p")
            if len(paragraphs) == 0:
                paragraphs = review_block[0].text.split('\n')
                flg_txt = True
            for paragraph in paragraphs:
                try:
                    if flg_txt and paragraph != '': 
                        title = "Overview"
                        if title not in review_char["text"]:
                            review_char["text"][title] = []
                        review_char["text"][title].append(paragraph)
                    elif paragraph == '':
                        continue
                    else:
                        title = paragraph.find_element(by=By.TAG_NAME, value="ul")
                        review_char["text"][title.text] = {}
                except:
                    review_char["text"][title.text] = paragraph.text
            pros_cons = reviews.find_elements(by=By.CLASS_NAME, value="stack-inline")
            pros_cons = pros_cons[0].find_elements(by=By.CLASS_NAME, value="col-12")
            for pro_con in pros_cons:
                title = pro_con.find_element(by=By.TAG_NAME, value="span")
                items = pro_con.find_elements(by=By.TAG_NAME, value="li")
                for item in items:
                    review_char[title.text].append(item.text)

            review_dict[url] = review_char
            driver.close()
            driver.quit()
        except Exception as e:
            urlss.append(url)
            print(e)

        i += 1
        print(i)
        break
    
    with open('./data/mobiles/mainpage/reviews.json', 'w', encoding='UTF-8') as f:
        json.dump(review_dict, f, indent=4, ensure_ascii=False)
    with open('./data/mobiles/urls/urls_err_reviews.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, indent=4, ensure_ascii=False)
main()