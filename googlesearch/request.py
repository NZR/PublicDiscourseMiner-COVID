from pytrends import dailydata
import json


# function to add to JSON
def write_json(data, outfile):
    with open(outfile, 'w') as f:
        json.dump(data, f, indent=4)


def create_jsonfile(filename, categories):
    output = {"category": {}}
    with open(filename, 'w') as outfile:
        json.dump(output, outfile, indent=4)

    for category in categories:
        with open(filename) as json_file:
            data = json.load(json_file)
            temp = data['category']
            temp[category] = {}
            temp[category]['word'] = {}
            temp[category]['bigram'] = {}
        write_json(data, filename)


def trend_lookup(filename, category, word_bigram, is_word, start_year, start_month, end_year, end_month, language):

    print("fetching ", word_bigram)
    df = dailydata.get_daily_data(word_bigram, start_year, start_month, end_year, end_month, language)

    with open(filename) as json_file:
        data = json.load(json_file)
        temp = data['category'][category]
        if is_word:
            temp['word'][word_bigram] = json.loads(df.to_json())[word_bigram]
        else:
            temp['bigram'][word_bigram] = json.loads(df.to_json())[word_bigram]
        write_json(data, filename)


# for bigram in wordsandbigrams['category'][category]['bigram']:
#     print("fetching ", bigram)
#     df2 = dailydata.get_daily_data(bigram, START_YEAR, START_MONTH, END_YEAR, END_MONTH, LANGUAGE)
#     with open(OUTFILE) as json_file:
#         data = json.load(json_file)
#         temp = data['category'][category]
#         temp['bigram'][bigram] = json.loads(df2.to_json())[bigram]
#     write_json(data)
#     df2 = df2.iloc[0:0]

