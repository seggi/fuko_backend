import json 

def convert_currencies_json_file():
    with open('api/utils/json/currencies.json') as json_file:
        data =  json.load(json_file)
        return data

def convert_budget_file():
    with open('api/utils/json/budget_categories.json') as json_file:
        data =  json.load(json_file)
        return data