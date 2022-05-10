import json 

def convert_currencies_json_file():
    with open('api/utils/currencies.json') as json_file:
        data =  json.load(json_file)
        return data