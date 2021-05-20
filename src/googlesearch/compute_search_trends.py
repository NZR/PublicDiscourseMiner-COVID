import json
import request

START_MONTH = 6  # including this month
END_MONTH = 11  # including this month
START_YEAR = 2020
END_YEAR = 2020
LANGUAGE = 'NL'
INFILE = "./input/wordsandbigrams.json"
OUTFILE = "./output/words2.json"

categories = ["8) Other (partly) complot theories"]


# request.create_jsonfile(OUTFILE, categories)

for category in categories:
    with open(INFILE) as json_file:
        data = json.load(json_file)
        for word in data['category'][category]['word']:
            request.trend_lookup(OUTFILE, category, word, True, START_YEAR, START_MONTH, END_YEAR, END_MONTH, LANGUAGE)
        for bigram in data['category'][category]['bigram']:
            request.trend_lookup(OUTFILE, category, bigram, False, START_YEAR, START_MONTH, END_YEAR, END_MONTH, LANGUAGE)

