import concurrent.futures
from selectolax.parser import HTMLParser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import json

links = ["https://www.91mobiles.com/tabletfinder.php", "./data/tablets/urls/urls.json", "./data/tablets/mainpage/keys.json"]

def get_list(lst):
    ret = []
    for item in lst:
        ret.append(item.text)
    return ret[0]

def get_attr(driver, cell):
    key_spec = {}
    flg_exist_model = len(cell.find_elements(by=By.CLASS_NAME, value="title_ul")) > 0
    flg_exist_os = len(cell.find_elements(by=By.CLASS_NAME, value="os_icon_cat")) > 0
    flg_exist_rate = len(cell.find_elements(by=By.CLASS_NAME, value="rating_box_new_list")) > 0
    flg_exist_price = len(cell.find_elements(by=By.CLASS_NAME, value="price_padding")) > 0

    model_lst = None
    os_version_lst = None
    rating_lst = None
    price_lst = None

    if flg_exist_model:
        model_lst = cell.find_elements(by=By.CLASS_NAME, value="title_ul")
        url = model_lst[0].find_elements(by=By.CSS_SELECTOR, value="a")
        model_lst = get_list(model_lst)
        url = url[0].get_attribute("href")

    if flg_exist_os:
        os_version_lst = cell.find_elements(by=By.CLASS_NAME, value="os_icon_cat")
        os_version_lst = get_list(os_version_lst)

    if flg_exist_rate:
        rating_lst = cell.find_elements(by=By.CLASS_NAME, value="rating_box_new_list")
        rating_lst = get_list(rating_lst)

    if flg_exist_price:
        price_lst = cell.find_elements(by=By.CLASS_NAME, value="price_padding")
        price_lst = get_list(price_lst)

    key_spec_cell = cell.find_elements(by=By.CLASS_NAME, value="grey_bar_custpage")

    
    for keycell in key_spec_cell:
        tmp = keycell.find_elements(by=By.CLASS_NAME, value="specs_li")
        for tmp2 in tmp:
            key = tmp2.text.split()[0]
            values = tmp2.text.split('\n')[1:]
            flg_exist= len(tmp2.find_elements(by=By.CLASS_NAME, value="mtr_bar_div")) > 0
            rate = None
            if flg_exist:
                rate = tmp2.find_element(by=By.CLASS_NAME, value="mtr_bar_div")
                rate = rate.find_elements(by=By.CSS_SELECTOR, value="div")
                rate = rate[0].get_attribute("style").split(': ')[1].split('%')[0]
            tmp_dict = {
                "values": values,
                "rate": rate
            }
            if key in key_spec:
                key_spec[key].append(tmp_dict)
            else:
                key_spec[key] = []
                key_spec[key].append(tmp_dict)
    ret = {
        "model": model_lst,
        "os_version": os_version_lst,
        "rating": rating_lst,
        "price": price_lst,
        "key_spec_cell": key_spec
        }
    return ret, url

def search(link):
    page = 1
    options = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
    urls = []
    cells_frmt = []
    driver.get(link[0])
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

    while len(driver.find_elements(by=By.CLASS_NAME, value="listing-btns4")) > 0:
        
        nxt_btn = driver.find_elements(by=By.CLASS_NAME, value="listing-btns4")
        nxt_btn = nxt_btn[0].find_elements(by=By.CLASS_NAME, value="list-bttnn")

        cells = driver.find_elements(by=By.CLASS_NAME, value="filer_finder")

        for cell in cells:
            cell_frmt, url = get_attr(driver, cell)
            urls.append(url)
            cells_frmt.append(cell_frmt)
        
        nxt_btn[0].click()
        time.sleep(10)
        print(page)
        page += 1

    with open(link[1], "w") as f:
        json.dump(urls, f, indent=4, ensure_ascii=False)
    
    with open(link[2], "w") as f:
        json.dump(cells_frmt, f, indent=4, ensure_ascii=False)

    driver.close()
    driver.quit()
    
    return [urls, cells_frmt]

def main():
    print("init")
    
    results = search(links)

main()