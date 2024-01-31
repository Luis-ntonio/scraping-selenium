import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

import time

with open('./data/mobiles/fullspecs/models_fix.json') as f:
    mobiles = json.load(f)

with open('./data/mobiles/fullspecs/err_models.json') as f:
    err = json.load(f)

with open('./data/mobiles/urls/urls.json') as f:
    urls = json.load(f)

options = webdriver.ChromeOptions()

for er in err:
    model = er.replace(' ', '-')
    model = model.lower()
    for url in urls:
        model = 'https://www.91mobiles.com/colors-win-w10-price-in-india'
        if model in url:
            driver = webdriver.Remote(command_executor="http://localhost:4444", options=options)
            driver.get(url)
            
            box_desc = {}
            flg_exist_specs = len(driver.find_elements(by=By.ID, value="specifications")) > 0
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
            mobiles[er]["specs"] = box_desc
            driver.close()
            driver.quit()
            print("next")
            break
with open('./data/mobiles/fullspecs/models_fix.json', "w", encoding='utf-8') as f:
    json.dump(mobiles, f, indent=4, ensure_ascii=False)
