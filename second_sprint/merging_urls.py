import json 



def main():
    with open ('./data/mobiles/urls/final_urls.json') as f:
        urls = json.load(f)
    with open('./data/mobiles/urls/urls.json') as f:
        urls_ = json.load(f)
    
    missing_urls = [url for url in urls_ if url not in urls]
    with open('./data/mobiles/urls/finals_urls.json', 'w', encoding='UTF-8') as f:
        json.dump(missing_urls, f, indent=4, ensure_ascii=False)

main()