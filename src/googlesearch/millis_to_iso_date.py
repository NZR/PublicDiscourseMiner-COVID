import datetime as DT
import json

inputfile = "output/words2.json"
outputfile = "output/google_trends.json"
categories = ["1) Person (referred to in conspiracy theories)", "2) Person involved in fake news fabrication",
              "3) Fakenews movement", "4) Other disease", "5) Vaccin discourage term",
              "6) Accusatory term for corona protagonist", "8) Other (partly) complot theories"]

outputjson = {"category": {}}

with open(inputfile) as json_file:
    data = json.load(json_file)
    for category in categories:
        outputjson['category'][category] = {"word": {}, "bigram": {}}
        for word in data['category'][category]['word']:
            outputjson['category'][category]['word'][word] = {}
            for date in list(data['category'][category]['word'][word].keys()):
                outputjson['category'][category]['word'][word][DT.datetime.utcfromtimestamp(int(date[:-3])).isoformat()] = data['category'][category]['word'][word][date]
        for bigram in data['category'][category]['bigram']:
            outputjson['category'][category]['bigram'][bigram] = {}
            for date in list(data['category'][category]['bigram'][bigram].keys()):
                outputjson['category'][category]['bigram'][bigram][DT.datetime.utcfromtimestamp(int(date[:-3])).isoformat()] = data['category'][category]['bigram'][bigram][date]

with open(outputfile, 'w') as output_file:
    json.dump(outputjson, output_file, indent=4)
