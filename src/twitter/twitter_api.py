from searchtweets import ResultStream, gen_rule_payload, load_credentials, collect_results
import json
import pickle

search_args = load_credentials(filename="twitter/api_creds.yaml",
                 yaml_key="search_tweets_api",
                 env_overwrite=False)


bigrams_string = []
words_string = []
bigram_count = {}
count = 0
with open('googlesearch/input/wordsandbigrams.json', 'r+') as file:
    bigrams = json.load(file)
    for k,v in bigrams["category"].items():
        for l,j in v.items():
            if l == "bigram":
                for item in j:
                    bigrams_string.append(item)
            else:
                for item in j:
                    words_string.append(item)

print(f'Words: {len(words_string)}')
print(f'Bigram: {len(bigrams_string)}')

grams = words_string #+ bigrams_string
print(len(grams))

item = 0
rules = {}
for i in range(1,30):
    rules[i] = "place_country:nl ("

for bi in grams:
    item = 1
    while (len(rules[item]) + len(bi)) > 126:
        item += 1
    rules[item] += f'"{bi}" OR '
remove=[]
for item, rule in rules.items():
    if len(rule) < 19:
        remove.append(item)
        continue
    rules[item] = rule[:-4] + ")"

for rem in remove:
    rules.pop(rem)

for k,v in rules.items():
    print(f'{len(v)}: {v}')

print(len(rules))

for key, bigram in rules.items():
    rule = gen_rule_payload(bigram, from_date="2020-06-01", to_date="2021-01-01") # testing with a sandbox account
    if key < 3:
        continue
    print(rule)
    try:
        tweets = collect_results(rule,
                                max_results=5000,
                                result_stream_args=search_args) # change this if you need to
    except:
        pass
    num_tweets = len(tweets)
    with open(f"twitter/output/{key}.json", "w+") as file:
        json.dump(tweets,file, indent=4)
    bigram_count[bigram] = f"{key} {num_tweets}"

with open(f'twitter/output/bigram_counts.json', "w+") as file:
    json.dump(bigram_count, file, indent=4)