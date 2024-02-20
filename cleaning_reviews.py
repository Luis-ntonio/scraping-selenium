import json


def main():
    with open('data/mobiles/fullspecs/model_reviews.json') as f:
        model_reviews = json.load(f)
    for model in model_reviews:
        model_reviews[model]['model'] = model_reviews[model]['model'].split('\n')[0].split(' (')[0]
        model_reviews[model]['review'] = model_reviews[model]['review'].split('\n')[-1]
    with open('data/mobiles/fullspecs/model_reviews_clean.json', 'w', encoding='UTF-8') as f:
        json.dump(model_reviews, f)


main()