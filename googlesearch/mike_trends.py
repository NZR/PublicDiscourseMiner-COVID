from pytrends.request import TrendReq
import pandas as pd
import json
import time



def get_grams():
    bigrams_string = []
    words_string = []
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
    grams = words_string + bigrams_string
    return grams

if __name__ == "__main__":
    pytrends = TrendReq()
    compare_list = [["viruswaarheid"],["bill gates"], ["corona"], ["staatsgreep"], ["bill gates", "viruswaarheid"], ["staatsgreep", "corona"]]
    grams = get_grams()
    for g in grams:
        temp = []
        temp.append(g)
        compare_list.append(temp)
    print(compare_list)
    timeframe = "2020-06-01 2020-12-01"
    geo = "NL"
    results = {}
    for comp in compare_list:
        comp_str = ""
        for c in comp:
            comp_str += c
        print(comp_str)
        results[comp_str] = {}
        try:
            for gram in grams:
                kwlist = comp.copy()
                kwlist.append(gram)
                print(kwlist)
                kwlist = list(set(kwlist))
                pytrends.build_payload(kw_list=kwlist,timeframe=timeframe, geo=geo)
                trend = pytrends.interest_over_time()
                results[comp_str][gram] = trend.to_csv(sep=';')
                time.sleep(1)
        finally:
            with open(f"googlesearch/output/{comp_str}.json", "w+") as file:
                json.dump(results,file,indent=4)




