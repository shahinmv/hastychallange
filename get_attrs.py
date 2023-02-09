import json

# load the JSON file
with open("Cable Cars Labels.json", "r") as file:
    data = json.load(file)

print(data['label_classes'][0]['class_id'])