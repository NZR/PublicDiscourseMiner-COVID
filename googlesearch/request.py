from pytrends import dailydata
import json

START_MONTH = 6 # including this month
END_MONTH = 11  # including this month
START_YEAR = 2020
END_YEAR = 2020
LANGUAGE = 'NL'


categories = ["1) Person (referred to in conspiracy theories)", "2) Person involved in fake news fabrication",
              "3) Fakenews movement", "4) Other disease", "5) Vaccin discourage term",
              "6) Accusatory term for corona protagonist", "8) Other (partly) complot theories"]

wordsandbigrams = json.load(open("./input/wordsandbigrams.json"))

output = {"category": {}}

for category in categories:
    output['category'][category] = {}
    for word in wordsandbigrams['category'][category]['word']:
        df = dailydata.get_daily_data(word, START_YEAR, START_MONTH, END_YEAR, END_MONTH, LANGUAGE)
        output['category'][category][word] = json.loads(df.to_json())[word]
    # for bigram in wordsandbigrams['category'][category]['bigram']:
    #     df2 = dailydata.get_daily_data(bigram, START_YEAR, START_MONTH, END_YEAR, END_MONTH, LANGUAGE)
    #     output['category'][category][bigram] = json.loads(df2.to_json())[bigram]

with open("./output/words.json") as outfile:
    json.dump(output, outfile)
