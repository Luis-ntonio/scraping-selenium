import concurrent.futures
from selectolax.parser import HTMLParser

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time
import json


options = webdriver.ChromeOptions()



def mains(urls): 
    models_box = {}
    urls_err = []
    

    for url in urls:
        try:
            #print("Scraping: ", url)
            driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
            driver.get(url)
            key_spec = {}
            box_desc = {}
            flg_exist_model = len(driver.find_elements(by=By.CLASS_NAME, value="h1_pro_head")) > 0
            flg_exist_keys = len(driver.find_elements(by=By.CLASS_NAME, value="key_specs_box")) > 0
            flg_exist_pro_rate = len(driver.find_elements(by=By.CLASS_NAME, value="rt_cn")) > 0
            flg_exist_user_rate = len(driver.find_elements(by=By.CLASS_NAME, value="usr_cn")) > 0
            flg_exist_pros = len(driver.find_elements(by=By.CLASS_NAME, value="proxBox")) > 0
            flg_exist_cons = len(driver.find_elements(by=By.CLASS_NAME, value="consBox")) > 0
            flg_exist_specs = len(driver.find_elements(by=By.ID, value="specifications")) > 0
            print(flg_exist_model, flg_exist_keys, flg_exist_pro_rate, flg_exist_user_rate, flg_exist_pros, flg_exist_cons, flg_exist_specs)
            model = None
            keys = None
            pro_rate = None
            user_rate = None
            pros = None
            cons = None
            specs = None
            if flg_exist_model:
                model = driver.find_elements(by=By.CLASS_NAME, value="h1_pro_head")
                model = model[0].text
            if flg_exist_keys:
                keys = driver.find_elements(by=By.CLASS_NAME, value="key_specs_box")
                flg_os = len(driver.find_elements(by=By.CLASS_NAME, value="for_list_li")) > 0
                os_version = None
                if flg_os:
                    os_version = driver.find_elements(by=By.CLASS_NAME, value="for_list_li")
                    os_version = os_version[0].text
                key_specs_box = keys[0].find_elements(by=By.CLASS_NAME, value="specs_ul")
                for key in key_specs_box:
                    flg_exist= len(key.find_elements(by=By.CLASS_NAME, value="mtr_bar_div")) > 0
                    rateing = None
                    characteristic = key.find_elements(by=By.CLASS_NAME, value="spcedHead")
                    characteristic = characteristic[0].text.split('\n')[0]
                    if flg_exist:
                        rateing = key.find_elements(by=By.CLASS_NAME, value="mtr_bar_div")
                        rateing = rateing[0].find_elements(by=By.CSS_SELECTOR, value="div")
                        rateing = rateing[0].get_attribute("style").split(': ')[1].split('%')[0]
                    key_specs = key.find_elements(by=By.CSS_SELECTOR, value="label")
                    key_specs = [spec.text for spec in key_specs]
                    tmp_dict = {
                        "values": key_specs,
                        "rate": rateing
                    }
                    if characteristic in key_spec:
                        key_spec[characteristic].append(tmp_dict)
                    else:
                        key_spec[characteristic] = []
                        key_spec[characteristic].append(tmp_dict)
            if flg_exist_pro_rate:
                pro_rate = driver.find_elements(by=By.CLASS_NAME, value="rt_cn")
                rt_pt = pro_rate[0].find_elements(by=By.CLASS_NAME, value="rt_pt")
                rt_pt = rt_pt[0].text
                out5 = pro_rate[0].find_elements(by=By.CLASS_NAME, value="out5")
                out5 = out5[0].text
                pro_rate = rt_pt + out5
            if flg_exist_user_rate:
                user_rate = driver.find_elements(by=By.CLASS_NAME, value="usr_cn")
                rt_pt = user_rate[0].find_elements(by=By.CLASS_NAME, value="rt_pt")
                rt_pt = rt_pt[0].text
                out5 = user_rate[0].find_elements(by=By.CLASS_NAME, value="out5")
                out5 = out5[0].text
                ovrate = user_rate[0].find_elements(by=By.CSS_SELECTOR, value="b")
                ovrate = ovrate[0].text
                user_rate = rt_pt + out5 + " (over " + ovrate + " rates)"
            if flg_exist_pros:
                pros = driver.find_elements(by=By.CLASS_NAME, value="proxBox")
                pros = pros[0].find_elements(by=By.CSS_SELECTOR, value="li")
                pros = [pro.text for pro in pros]
            if flg_exist_cons:
                cons = driver.find_elements(by=By.CLASS_NAME, value="consBox")
                cons = cons[0].find_elements(by=By.CSS_SELECTOR, value="li")
                cons = [con.text for con in cons]
            if flg_exist_specs:
                specs = driver.find_elements(by=By.ID, value="specifications")
                spec_box = specs[0].find_elements(by=By.CLASS_NAME, value="spec_box")
                for box in spec_box:
                    spec = box.find_elements(by=By.CLASS_NAME, value="specHead")
                    spec = spec[0].text
                    lft = box.find_elements(by=By.CLASS_NAME, value="spcsLeft")
                    flg_rate = len(lft[0].find_elements(by=By.CLASS_NAME, value="hd_tlt")) > 0
                    rate = None
                    if flg_rate:
                        rate = lft[0].find_elements(by=By.CLASS_NAME, value="mtr_bar_div")
                        rate = rate[0].find_elements(by=By.CSS_SELECTOR, value="div")
                        rate = rate[0].get_attribute("style").split(': ')[1].split('%')[0]
                    desc = box.find_elements(by=By.CLASS_NAME, value="spec_table")
                    desc = desc[0].find_elements(by=By.CSS_SELECTOR, value="tbody")
                    desc = desc[0].find_elements(by=By.CSS_SELECTOR, value="tr")
                    box_desc[spec] = {"rate": rate, "Description": {}}
                    is_sub = False
                    for tr in desc:
                        flg_subtitle = len(tr.find_elements(by=By.CLASS_NAME, value="mnhead")) > 0
                        if flg_subtitle:
                            is_sub = True
                            subdesc = tr.find_elements(by=By.CLASS_NAME, value="mnhead")
                            subdesc = subdesc[0].text
                            box_desc[spec]["Description"][subdesc] = {}
                        else:
                            specs_rate = None
                            title = tr.find_elements(by=By.CLASS_NAME, value="spec_ttle")
                            title = title[0].text
                            specs = tr.find_elements(by=By.CLASS_NAME, value="spec_des")
                            flg_multispec = len(specs[0].find_elements(by=By.CLASS_NAME, value="sim_lft")) > 0
                            flg_rate = len(specs[0].find_elements(by=By.CLASS_NAME, value="select_arrow")) > 0
                            if flg_multispec:
                                multispec = {}
                                specs_sub = specs[0].find_elements(by=By.CLASS_NAME, value="sim_lft")
                                specs_desc = specs[0].find_elements(by=By.CLASS_NAME, value="sim_rft")
                                specs_sub = [spec.text for spec in specs_sub]
                                specs_desc = [spec.text for spec in specs_desc]
                                for i in range(len(specs_sub)):
                                    tmp = specs_desc[i].split('\n')
                                    multispec[specs_sub[i]] = tmp
                                specs = multispec
                            elif flg_rate:
                                specs_rate = specs[0].find_elements(by=By.CLASS_NAME, value="select_arrow")
                                specs_rate = specs_rate[0].find_elements(by=By.CLASS_NAME, value="mtr_bar_div")
                                specs_rate = specs_rate[0].find_elements(by=By.CSS_SELECTOR, value="div")
                                specs_rate = specs_rate[0].get_attribute("style").split(': ')[1].split('%')[0]
                                specs = specs[0].text.split('\n')[0]
                                specs = {"Description": specs, "rate": specs_rate}
                            else:
                                specs = specs[0].text.split('\n')
                                if len(specs) == 1:
                                    specs = specs[0]
                            if is_sub:
                                box_desc[spec]["Description"][subdesc][title] = specs
                            else:
                                box_desc[spec]["Description"][title] = specs
            models_box[model] = {
                "keys": key_spec,
                "pro_rate": pro_rate,
                "user_rate": user_rate,
                "pros": pros,
                "cons": cons,
                "specs": box_desc
            }
            driver.close()
            driver.quit()
        except Exception as e:
            urls_err.append(url)
            driver.close()
            driver.quit()
    return models_box, urls_err
    
folder = input("Enter folder name: ")
with open(f'./{folder}/mobiles/urls/urls.json') as f:
    urls = json.load(f)
    
    models_box, urls_err = mains(urls)

with open(f"./{folder}/mobiles/fullspecs/models.json", "w", encoding='utf-8') as f:
    json.dump(models_box, f, indent=4, ensure_ascii=False)

with open(f"./{folder}/mobiles/urls/urls_err.json", "w", encoding='utf-8') as f:
    json.dump(urls_err, f, indent=4, ensure_ascii=False)
    