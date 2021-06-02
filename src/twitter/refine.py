import json
import re

tweets = []
for i in range(1,12):
    with open(f'twitter/place country output/{i}.json') as file:
        temp = json.load(file)
        for t in temp:
            tweets.append(t)
for i in range(1,7):
    with open(f'twitter/output/{i}.json') as file:
        temp = json.load(file)
        for t in temp:
            tweets.append(t)

refined = []
values = ["created_at", "text", "id", "quote_count", "reply_count", "retweet_count", "favorite_count"]
for t in tweets:
    temp = {}
    temp["categories"] = []
    for v in values:
        temp[v] = t[v]
    if t["truncated"]:
        temp["text"] = t["extended_tweet"]["full_text"]
    refined.append(temp)

with open("googlesearch/input/wordsandbigrams.json", "r") as file:
    grams = json.load(file)

cat = {}
for k,v in grams["category"].items():
    cat[k] = v["word"] + v["bigram"]


for t in refined:
    for k,v in cat.items():
        for gram in v:
            if " " in gram.strip():
                g = gram.lower().split(" ")
                re_str1 = f"{g[0]}.*{g[1]}"
                re_str2 = f"{g[1]}.*{g[0]}"
                # print(re_str1)
                if re.search(re_str1, t["text"].lower()) or re.search(re_str2, t["text"].lower()):
                    if k not in t["categories"]:
                        t["categories"].append(k)
            else:
                if gram in t["text"].lower():
                    if k not in t["categories"]:
                        t["categories"].append(k)
        
with open("twitter/cat_refined.json", "w") as file:
    json.dump(cat, file, indent=4)

with open("twitter/refined.json", "w+") as file:
    json.dump(refined,file,indent=4)
