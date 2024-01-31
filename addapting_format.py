import json
from fuzzywuzzy import fuzz

def main(folder):
    err_model = []
    with open(f'./{folder}/mobiles/fullspecs/models_fix.json') as f:
        mobiles = json.load(f)
        for mobile in mobiles:
            try:
                keys = mobiles[mobile]["keys"]
                full_table = mobiles[mobile]["specs"]
                if len(full_table.items()) == 0:
                    raise Exception("no specs")
                new_key = {}
                for key in keys:
                    key_val = keys[key][0]["values"]
                    if key == "Display":
                        temp = []
                        for k in key_val:
                            if ',' in k:
                                tmp = k.split(',')
                                for t in tmp:
                                    temp.append(t)
                            else:
                                temp.append(k)
                        key_val = temp
                    if key not in full_table:
                        if key == "Battery":
                            key = "Network & Connectivity"
                        else:
                            continue
                    values = full_table[key]["Description"]
                    rate = full_table[key]["rate"]

                    new_key[key] = {}
                    new_key[key]["rate"] = rate
                    new_key[key]["Description"] = {}

                    for char in key_val:
                        last_score = 0
                        last_key = ""
                        last_value = ""

                        for k, v in values.items():
                            end_iter = False
                            comp = v
                            if type(v) == dict:
                                if "Description" in v:
                                    comp = f"{v['Description']}"
                                else:
                                    end_iter = True

                                    for _k, _v in v.items():
                                        comp = f"{_v}"
                                        if type(v[_k]) == dict:
                                            comp = f"{v[_k]['Description']}"
                                        if type(v[_k]) == list:
                                            comp = ""
                                            for s in v[_k]:
                                                comp += f"{s} "
                                        if 'MP' in char:
                                            last_key = f"{k.capitalize()} Resolution"
                                            last_value = char
                                            break
                                        score = fuzz.ratio(comp + " " + _k + " " + k.lower(), char)
                                        if score >= last_score:
                                            last_score = score
                                            last_key = _k  
                                            last_value = char   

                            if end_iter == False:      
                                score = fuzz.ratio(k + " " + comp, char)
                                if score > last_score:
                                    last_score = score
                                    last_key = k  
                                    last_value = char   
                            else:
                                if last_key not in new_key[key]["Description"]:
                                    new_key[key]["Description"][last_key] = last_value
                        new_key[key]["Description"][last_key] = last_value
                mobiles[mobile]["keys"] = new_key
                #print(mobile)
            except Exception as e:
                print(e)
                err_model.append(mobile)
                continue
        return mobiles, err_model

if __name__ == "__main__":
    folder = input("Enter folder name: ")
    _json, err_m = main(folder)
    with open(f'./{folder}/mobiles/fullspecs/models_fixed.json', "w", encoding='utf-8') as f:
       json.dump(_json, f, indent=4, ensure_ascii=False)
    print(err_m)
    with open(f'./{folder}/mobiles/fullspecs/err_models.json', "w", encoding='utf-8') as f:
       json.dump(err_m, f, indent=4, ensure_ascii=False)