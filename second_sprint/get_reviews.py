import concurrent.futures

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium_stealth import stealth

from fake_useragent import UserAgent

import time
import json
import random

user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.71 Safari/537.36"

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
options.add_argument(f'user-agent={user_agent}')
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
driver = webdriver.Chrome(options=options)

review_dict = {}
urlss = []

def finding_b(paragraph, title_, flg_txt):
    if len(paragraph.find_elements(by=By.XPATH, value="./b")) != 0:
        pos_title = paragraph.find_elements(by=By.XPATH, value="./b")[0].text
    elif len(paragraph.find_elements(by=By.XPATH, value="./span")) != 0:
        pos_title = paragraph.find_elements(by=By.XPATH, value="./span")[0].text
    else:
        return False, title_, flg_txt
    loc = paragraph.text.find(pos_title)
    if 'FAQs' in pos_title or 'Frequently Asked Questions' in pos_title:
        pos_title = "FAQs"
    flg_int = False
    try:
        int(pos_title[0])
        pos_title = title_
        flg_int = True
        flg_txt = True
    except:
        pass
    if (loc == 0 and len(pos_title) < 40) and flg_int == False:
        
        return True, pos_title, flg_txt
    return False, title_, flg_txt

def main():
    
    i = 0
    with open('./data/mobiles/mainpage/urls.json') as f:
        urls = json.load(f)
        urls = ["https://pricebaba.com/mobile/samsung-galaxy-a9", "https://pricebaba.com/mobile/vivo-v21-5g-256gb", "https://pricebaba.com/mobile/lenovo-k80", "https://pricebaba.com/mobile/asus-zenfone-2-laser-ze601kl", "https://pricebaba.com/mobile/letv-le-2-pro-4gb-64gb"]
    for url in urls:
        

        print("Session ID:", driver.session_id)
        try:
            time.sleep(10)
            driver.get(url)
            time.sleep(10)
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
                    if cond and ('FAQs' in par.text or 'Frequently Asked Questions' in par.text):
                        cond = False
                    if len(par.find_elements(by=By.TAG_NAME, value="span")) != 0 or par.text == '' or cond:
                        spans += 1
                # Use the "spans" variable in the subsequent code
                print(spans, len(paragraphs))
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
                            if "Alternatives" in titles[j] :
                                review_char["text"][titles[j]] = []
                                for t in text[j:]:
                                    if ('FAQs' in t or 'Frequently Asked Questions' in t):
                                        break
                                    review_char["text"][titles[j]].append(t)
                            else:

                                if 'FAQs' in titles[j] or 'Frequently Asked Questions' in titles[j]:
                                    titles[j] = "FAQs"
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
                                if 'FAQs' in titles[j] or 'Frequently Asked Questions' in titles[j]:
                                    titles[j] = "FAQs"
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
                        if len(cant) > 2:
                            flg_allinone = True
                            flg_par = False
                        if len(cant) == 1:
                            flg_par = False
                        elif iter == 0:
                            iter = len(cant)
                        elif iter != len(cant):
                            flg_par = False
                        
                        flg_b, title_, flg_txt = finding_b(paragraph, title_, flg_txt)
                        
                        if flg_par != True:

                            if flg_allinone == True:
                                titles = paragraph.find_elements(by=By.XPATH, value="./span")
                                tmp = []
                                for title in titles:
                                    tmp.append(title.text)
                                titles = tmp
                                text = paragraph.text
                                tmp = text.split('\n')
                                cond_ = False
                                if len(tmp[0]) > 40:
                                    title = ["Overview"]
                                    for tit in titles:
                                        if tit not in tmp[0]:
                                            title.append(tit)
                                    titles = title
                                    cond_ = True

                                if cond_ == True:
                                    lst_titles = []
                                    for title in titles:
                                        if title == 'Overview' or len(title) < 40:
                                            lst_titles.append(title)
                                            text = text.replace(title, '')
                                    
                                    titles = lst_titles
                                    
                                    if titles[-1] == 'Overview':
                                        title_ = 'Overview'
                                    text = text.split('\n')
                                    text = [x for x in text if x != '']
                                    if len(titles) == 1:
                                        review_char["text"][titles[0]] = text
                                    else:
                                        for j in range(0, len(titles)):
                                            if "Alternatives" in titles[j]:
                                                review_char["text"][titles[j]] = []
                                                for t in text[j:]:
                                                    if ('FAQs' in t or 'Frequently Asked Questions' in t):
                                                        break
                                                    review_char["text"][titles[j]].append(t)
                                            else:
                                                if 'FAQs' in titles[j] or 'Frequently Asked Questions' in titles[j]:
                                                    titles[j] = "FAQs"
                                                review_char["text"][titles[j]] = [text[j]]
                                else:
                                    lst_titles = []
                                    for title in titles:
                                        if len(title) < 40:
                                            lst_titles.append(title)
                                            text = text.replace(title, '')
                                    titles = lst_titles
                                    text = text.split('\n')
                                    text = [x for x in text if x != '']
                                    if len(titles) == 1:
                                        review_char["text"][titles[0]] = text
                                    for j in range(0, len(titles)):
                                        if "Alternatives" in titles[j]:
                                            review_char["text"][titles[j]] = text[j:]
                                        else:
                                            if 'FAQs' in titles[j] or 'Frequently Asked Questions' in titles[j]:
                                                titles[j] = "FAQs"
                                            review_char["text"][titles[j]] = [text[j]]
                                    
                                flg_allinone = False
                                title = 0
                                if title_ != '':
                                    title = 1
                                else:
                                    title = 0
                                    title_ = 'No title'
                                continue
                            if paragraph.text == '':
                                continue

                            if 'Alternatives' in paragraph.text:
                                title_ = "Alternatives"
                                cond = True

                            if cond == True and ('FAQs' in paragraph.text or 'Frequently Asked Questions' in paragraph.text):
                                cond = False

                            if 'FAQs' in paragraph.text or 'Frequently Asked Questions' in paragraph.text:
                                flg = False
                                title = 1
                                title_ = "FAQs"
                                text = paragraph.text
                                text = text.replace(title_, '')
                                review_char["text"][title_] = []
                                if text != '':
                                    review_char["text"][title_] = text.split('\n')[1:]
                                continue
                            if (title_ == '' or title_ == "Overview") and (len(paragraph.text) > 40 and cond == False):
                                title = 1
                                title_ = "Overview"
                            
                            if len(paragraph.text) > 40:
                                title = 1

                            if flg == False and cond == False:
                                title = 1
                            
                            if flg_b == True:
                                title = 1

                            if title == 0 and cond == False:
                                if ('FAQs' in paragraph.text or 'Frequently Asked Questions' in paragraph.text):
                                    title_ = "FAQs"
                                    flg = False
                                title = 1
                                title_ = paragraph.find_elements(by=By.TAG_NAME, value="span")
                                if len(title_) == 1:
                                    title_ = title_[0].text
                                else:
                                    for title in title_:
                                        if title.text != '':
                                            title_ = title.text
                                            break
                                        

                            elif cond == True:
                                if title_ not in review_char["text"]:
                                    review_char["text"][title_] = []
                                else:
                                    review_char["text"][title_].append(paragraph.text)

                            else:
                                title = 0
                                if ('FAQs' in title_ or 'Frequently Asked Questions' in title_):
                                    
                                    text = paragraph.text.replace(title_, '')
                                    title_ = "FAQs"
                                else:
                                    if flg_b == True:
                                        text = paragraph.text.replace(title_, '')
                                        flg_b = False
                                    else:
                                        text = paragraph.text.replace(title_, '')

                                text = text.split('\n')
                                for t in text:
                                    if t != '':
                                        if title_ not in review_char["text"]:
                                            review_char["text"][title_] = []
                                        review_char["text"][title_].append(t)
                                
                        else:
                            block = paragraph.find_elements(by=By.XPATH, value="./span")
                            if block[0].text == "":
                                continue
                            title_ = block[0].text
                            text = block[1:]
                            if title_ not in review_char["text"]:
                                review_char["text"][title_] = []
                            for t in text:
                                review_char["text"][title_].append(t.text)

                else:   
                    flg_iter = True
                    title = ''
                    flg_txt = False
                    for paragraph in paragraphs:
                        flg_b, title, flg_txt = finding_b(paragraph, title, flg_txt)
                        iter = 0
                        try:
                            if flg_b == True:
                                if title == '': #omit blank spaces
                                    flg_b = False
                                    continue
                                text = paragraph.text 
                                text = text.replace(title, '')
                                if title == 'FAQs' and flg_txt == False:
                                    review_char["text"][title] = []
                                    flg_txt = True
                                elif text != '':
                                    text = text.split('\n')
                                    
                                    for t in text:
                                        if t != '':
                                            review_char["text"][title].append(t)
                                    flg_txt = False
                                else:
                                    review_char["text"][title] = []
                                    flg_txt = True
                                flg_b = False
                                continue
                            if paragraph.text == '': #omit blank spaces
                                continue

                            elif flg_txt == True:
                                review_char["text"][title].append(paragraph.text)
                                continue

                            elif len(paragraph.find_elements(by=By.TAG_NAME, value="span")) != 0 and flg_iter and 'FAQs' not in title and 'Frequently Asked Questions' not in title: #if the paragraph has a span tag
                                title = paragraph.find_element(by=By.TAG_NAME, value="span").text
                                text = paragraph.text
                                text = text.replace(title, '')
                                if text != '':
                                    review_char["text"][title] = text.split('\n')[1:]
                                else:
                                    review_char["text"][title] = []
                                    flg_iter = False

                            elif iter == 0 and title == '' and len(paragraph.find_elements(by=By.TAG_NAME, value="u")) == 0 and flg_iter and 'FAQs' not in title and 'Frequently Asked Questions' not in title: #if the paragraph has no u tag and is first paragraph
                                title = "Overview"
                                text = paragraph.text.split('\n')
                                if title not in review_char["text"]:
                                    review_char["text"][title] = []
                                    for t in text:
                                        if t != '':
                                            review_char["text"][title].append(t)
                                else:
                                    for t in text:
                                        if t != '':
                                            review_char["text"][title].append(t)
                                iter += 1
                            elif 'FAQs' in paragraph.text or 'Frequently Asked Questions' in paragraph.text:
                                title = "FAQs"
                                review_char["text"][title] = []
                                flg_iter = False
                            elif len(paragraph.find_elements(by=By.TAG_NAME, value="u")) != 0 and 'FAQs' not in title and 'Frequently Asked Questions' not in title: #if the paragraph has a u tag
                                title = paragraph.find_element(by=By.TAG_NAME, value="u").text
                                review_char["text"][title] = []
                                flg_iter = False

                            elif len(paragraph.find_elements(by=By.TAG_NAME, value="u")) == 0 and flg_iter and 'FAQs' not in title and 'Frequently Asked Questions' not in title: #if the paragraph has no u tag
                                title = paragraph.find_element(by=By.TAG_NAME, value="span").text
                                if title not in review_char["text"]:
                                    review_char["text"][title] = []

                            else:
                                text = paragraph.text
                                text = text.split('\n')
                                for t in text:
                                    if t != '':
                                        review_char["text"][title].append(t)
                                flg_iter = True
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

        except Exception as e:
            urlss.append(url)
            print(url)
            print(e)


        i += 1
        print(i)
        break
    with open('./data/mobiles/mainpage/reviews4.json', 'w', encoding='UTF-8') as f:
        json.dump(review_dict, f, indent=4, ensure_ascii=False)
    with open('./data/mobiles/urls/urls_err_reviews3.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, indent=4, ensure_ascii=False)
main()