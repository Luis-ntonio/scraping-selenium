import json

def get_key_dict():
    with open('./data/mobiles/mainpage/reviews.json', encoding='utf-8') as f:
        dict_ = json.load(f)
    urlss = []
    for key in dict_.keys():
        urlss.append(key)
    print(urlss)
    with open('./data/mobiles/mainpage/urls.json', 'w', encoding='UTF-8') as f:
        json.dump(urlss, f, ensure_ascii=False, indent=4)
get_key_dict()