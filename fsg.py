import json

with open('data.json', 'r') as file:
    data = json.load(file)
    for i in data:
        print(i['current_dict'])