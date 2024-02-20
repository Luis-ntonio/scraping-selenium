import json
from fuzzywuzzy import fuzz

models = []

def main():
    i= 0
    with open('data/mobiles/fullspecs/model_reviews_clean.json') as f:
        model_reviews = json.load(f)
    for model in model_reviews:
        score = fuzz.ratio(model.upper(), model_reviews[model]['model'].upper())
        if score < 85:
            models.append(model)
    for model in models:
        del model_reviews[model]

    with open('data/mobiles/fullspecs/model_reviews_cleaned.json', 'w', encoding='UTF-8') as f:
        json.dump(model_reviews, f)
with open('data/mobiles/fullspecs/models_fixed.json') as f:
        model_reviews = json.load(f)
        print(len(model_reviews))