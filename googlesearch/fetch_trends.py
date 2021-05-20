from pytrends.request import TrendReq
import pandas as pd
import time
import json

# Based on: https://www.honchosearch.com/blog/seo/how-to-use-python-pytrends-to-automate-google-trends-data/

startTime = time.time()
pytrend = TrendReq(hl='nl-NL', tz=360)

categories = ["1) Person (referred to in conspiracy theories)", "2) Person involved in fake news fabrication",
              "3) Fakenews movement", "4) Other disease", "5) Vaccin discourage term",
              "6) Accusatory term for corona protagonist", "8) Other (partly) complot theories"]

wordsandbigrams = json.load(open("./input/wordsandbigrams.json"))

df2 = []  # list with searchterms

for category in categories:
    df2.append(wordsandbigrams['category'][category]['word'])
    df2.append(wordsandbigrams['category'][category]['bigram'])

dataset = []
print(df2)
for x in range(0, len(df2)):
    keywords = df2[x]
    print(keywords)
    pytrend.build_payload(
        kw_list=keywords,
        cat=0,
        timeframe='2020-06-01 2020-12-01',
        geo='NL')
    data = pytrend.interest_over_time()
    if not data.empty:
        data = data.drop(labels=['isPartial'], axis='columns')
        dataset.append(data)

result = pd.concat(dataset, axis=1)
result.to_csv('search_trends.csv')

executionTime = (time.time() - startTime)
print('Execution time in sec.: ' + str(executionTime))
