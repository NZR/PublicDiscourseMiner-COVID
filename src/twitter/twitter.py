import json

with open("twitter/output/test/last month.json", "r+") as file:
    j = json.load(file)

print(len(j))