import json

def remove_duplicates(input_list):
    unique_items = set()
    result_list = []

    for item in input_list:
        if item not in unique_items:
            unique_items.add(item)
            result_list.append(item)

    return result_list

links = [["./data/tablets/mainpage/keys.json", "./data/tablets/urls/urls.json"], ["./data/mobiles/mainpage/keys.json", "./data/mobiles/urls/urls.json"]]

def main(link):
    ret = []
    unique_items = set()
    result_list = []
    with open(link[0]) as f:

        keys = json.load(f)
        for key in keys:
            if key['model'] not in unique_items:
                unique_items.add(key['model'])
                result_list.append(key)
        print("Lista original:", len(keys))
        print("Lista sin duplicados:", len(result_list))

    with open(link[0], "w", encoding='utf-8') as f:
        json.dump(result_list, f, indent=4, ensure_ascii=False)

    with open(link[1]) as f:
        urls = json.load(f)
        list_without_duplicates = remove_duplicates(urls)

        print("Lista original:", len(urls))
        print("Lista sin duplicados:", len(list_without_duplicates))

    with open(link[1], "w", encoding='utf-8') as f:
        json.dump(list_without_duplicates, f, indent=4, ensure_ascii=False)

for link in links:
    main(link)