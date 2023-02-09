import json

# load the JSON file
with open("Cable Cars Labels.json", "r") as file:
    data = json.load(file)

# get the names of the attributes in the JSON file
attribute_names = list(data.keys())

print("Attribute names:", attribute_names)

