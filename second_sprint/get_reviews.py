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


review_dict = {}
urlss = []
def main():
    i = 0
    with open('./data/mobiles/mainpage/urls.json') as f:
        urls = json.load(f)
        urls = ["https://pricebaba.com/mobile/micromax-canvas-nitro-3-e352", "https://pricebaba.com/mobile/lenovo-a2020", "https://pricebaba.com/mobile/lava-x81", "https://pricebaba.com/mobile/karbonn-titanium-mach-six", "https://pricebaba.com/mobile/micromax-bolt-a082", "https://pricebaba.com/mobile/panasonic-eluga-note"]
    for url in urls:
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
        print("Session ID:", driver.session_id)
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
            more = reviews.find_elements(by=By.TAG_NAME, value="label")
            if len(more) != 0:
                more[0].click()
            review_block = reviews.find_elements(by=By.CLASS_NAME, value="detail-desc")
            if len(review_block) != 0:
                paragraphs = review_block[0].find_elements(by=By.TAG_NAME, value="p")
                spans = 0
                cond = False
                for par in paragraphs:
                    if 'Alternatives' in par.text:
                        cond = True
                    if cond and 'FAQs' in par.text:
                        cond = False
                    if len(par.find_elements(by=By.TAG_NAME, value="span")) != 0 or par.text == '' or cond:
                        spans += 1
                # Use the "spans" variable in the subsequent code
                if len(paragraphs) == 0:
                    paragraphs = review_block[0].text.split('\n')
                    for paragraph in paragraphs:
                        if paragraph != '':
                                title = "Overview"
                                if title not in review_char["text"]:
                                    review_char["text"][title] = []
                                review_char["text"][title].append(paragraph)
                elif len(paragraphs) == 1:
                    titles = paragraphs[0].find_elements(by=By.TAG_NAME, value="span")
                    text = paragraphs[0].text
                    tmp = text.split('\n')
                    cond = False
                    if len(tmp[0]) > 40:
                        title = ["Overview"]
                        title.extend([title.text for title in titles])
                        titles = title
                        cond = True
                    if cond:
                        for title in titles:
                            text = text.replace(title, '')
                        text = text.split('\n')
                        text = [x for x in text if x != '']
                        for j in range(0, len(titles)):
                            if titles[j] == "Alternatives":
                                review_char["text"][titles[j]] = []
                                for t in text[j:]:
                                    if 'FAQs' in t:
                                        break
                                    review_char["text"][titles[j]].append(t)
                            else:
                                review_char["text"][titles[j]] = [text[j]]
                    else:
                        for title in titles:
                            text = text.replace(title.text, '')
                        text = text.split('\n')
                        text = [x for x in text if x != '']
                        for j in range(0, len(titles)):
                            if titles[j].text == "Alternatives":
                                review_char["text"][titles[j].text] = text[j:]
                            else:
                                review_char["text"][titles[j].text] = [text[j]]
                
                elif len(paragraphs) == spans:
                    title = 0
                    title_ = ''
                    flg = True
                    cond = False
                    flg_par = True
                    iter = 0
                    flg_allinone = False
                    for paragraph in paragraphs:
                        cant = paragraph.find_elements(by=By.XPATH, value="./span")
                        if paragraph.text == '':
                            continue
                        if len(cant) > 2:
                            flg_allinone = True
                            flg_par = False
                            break
                        if len(cant) == 1:
                            flg_par = False
                            break
                        elif iter == 0:
                            iter = len(cant)
                        elif iter != len(cant):
                            flg_par = False
                            break
                    for paragraph in paragraphs:
                        if flg_par != True:
                            if flg_allinone == True:
                                titles = paragraph.find_elements(by=By.TAG_NAME, value="span")
                                text = paragraph.text
                                tmp = text.split('\n')
                                cond = False
                                if len(tmp[0]) > 40:
                                    title = ["Overview"]
                                    title.extend([title.text for title in titles])
                                    titles = title
                                    cond = True
                                if cond == True:
                                    for title in titles:
                                        text = text.replace(title, '')
                                    text = text.split('\n')
                                    text = [x for x in text if x != '']
                                    for j in range(0, len(titles)):
                                        if "Alternatives" in titles[j]:
                                            review_char["text"][titles[j]] = []
                                            for t in text[j:]:
                                                if 'FAQs' in t:
                                                    break
                                                review_char["text"][titles[j]].append(t)
                                        else:
                                            review_char["text"][titles[j]] = [text[j]]
                                else:
                                    for title in titles:
                                        text = text.replace(title.text, '')
                                    text = text.split('\n')
                                    text = [x for x in text if x != '']
                                    for j in range(0, len(titles)):
                                        if "Alternatives" in titles[j].text:
                                            review_char["text"][titles[j].text] = text[j:]
                                        else:
                                            review_char["text"][titles[j].text] = [text[j]]
                                flg_allinone = False
                                title = 0
                                title_ = 'no_title'
                                continue
                            if paragraph.text == '':
                                continue
                            if 'Alternatives' in paragraph.text:
                                title_ = "Alternatives"
                                cond = True
                            if cond == True and 'FAQs' in paragraph.text:
                                cond = False
                            if (title_ == '' or title_ == "Overview") and (len(paragraph.text) > 25 and cond == False):
                                title = 1
                                title_ = "Overview"
                            if flg == False and cond == False:
                                title = 1
                            if title == 0 and cond == False:
                                if "FAQs" in paragraph.text:
                                    flg = False
                                title = 1
                                title_ = paragraph.find_element(by=By.TAG_NAME, value="span")
                            elif cond == True:
                                if title_ not in review_char["text"]:
                                    review_char["text"][title_] = []
                                else:
                                    review_char["text"][title_].append(paragraph.text)
                            else:
                                title = 0
                                if "FAQs" in title_.text:
                                    if type(title_) == str:
                                        text = paragraph
                                    else:

                                        text = paragraph
                                else:
                                    text = paragraph.find_element(by=By.TAG_NAME, value="span")
                                if type(title_) == str:
                                    if title_ not in review_char["text"]:
                                        review_char["text"][title_] = text.text.split('\n')

                                    else:
                                        review_char["text"][title_].append(text.text)
                                else:
                                    if title_.text not in review_char["text"]:
                                       review_char["text"][title_.text] = text.text.split('\n')

                                    else:
                                        review_char["text"][title_.text].append(text.text)
                        else:
                            block = paragraph.find_elements(by=By.XPATH, value="./span")
                            if block[0].text == "":
                                continue
                            title_ = block[0]
                            text = block[1:]
                            if title_.text not in review_char["text"]:
                                review_char["text"][title_.text] = []
                            for t in text:
                                review_char["text"][title_.text].append(t.text)

                else:   
                    flg_iter = True
                    for paragraph in paragraphs:
                        iter = 0
                        try:
                            
                            if paragraph.text == '':
                                continue
                            elif len(paragraph.find_elements(by=By.TAG_NAME, value="span")) != 0 and flg_iter:
                                title = paragraph.find_element(by=By.TAG_NAME, value="span")
                                text = paragraph.text
                                text = text.replace(title.text, '')
                                review_char["text"][title.text] = text.split('\n')[1:]
                            elif iter == 0 and len(paragraph.find_elements(by=By.TAG_NAME, value="u")) == 0 and flg_iter:
                                title = "Overview"
                                if title not in review_char["text"]:
                                    review_char["text"][title] = paragraph.text.split('\n')
                                else:
                                    review_char["text"][title].append(paragraph.text)
                                iter += 1
                            elif len(paragraph.find_elements(by=By.TAG_NAME, value="u")) != 0:
                                title = paragraph.find_element(by=By.TAG_NAME, value="u")
                                review_char["text"][title.text] = []
                                flg_iter = False
                            elif len(paragraph.find_elements(by=By.TAG_NAME, value="u")) == 0 and flg_iter:
                                title = paragraph.find_element(by=By.TAG_NAME, value="span")
                                if title.text not in review_char["text"]:
                                    review_char["text"][title.text] = []
                            else:
                                review_char["text"][title.text].append(paragraph.text)
                        except Exception as e:
                            pass
            pros_cons = reviews.find_elements(by=By.CLASS_NAME, value="stack-inline")
            if len(pros_cons) != 0:
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
            print(url)
            print(e)


        i += 1
        print(i)
    
    with open('./data/mobiles/mainpage/reviews3.json', 'w', encoding='UTF-8') as f:
        json.dump(review_dict, f, indent=4, ensure_ascii=False)
    with open('./data/mobiles/urls/urls_err_reviews.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, indent=4, ensure_ascii=False)
main()