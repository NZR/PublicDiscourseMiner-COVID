import json
from mike_trends import get_grams
import pandas as pd
from io import StringIO
import plotly.express as px


INFILE = "googlesearch/output/staatsgreepcorona.json"

with open(INFILE) as json_file:
    data = json.load(json_file)
    for k,v in data.copy().items():
        for l,j in v.items():
            df_str = StringIO(j)
            df = pd.read_csv(df_str, sep=";")
            data[k][l] = df

terms = list(data.keys())
grams = get_grams()

def get_distance(df, gram, term):
   return abs((df[term] - df[gram]).sum())

def get_terms_combined(grams,terms):
    min_dist_term = {}
    for gram in grams:
        min_dist = 1000000 #enorm hoog
        for term in terms:
            for t in term.split(";"):
                df = data[t][gram]
                dist = get_distance(df, gram, t)
                if dist < min_dist:
                    if t == gram:
                        continue
                    min_term = t
                    min_dist = dist
        if not min_term in min_dist_term:
            min_dist_term[min_term] = {}
        min_dist_term[min_term][gram] = min_dist
    return min_dist_term


def create_dataframe(term, grams, data):
    df = data[term][grams[0]]
    df = df.drop(columns = "isPartial")
    # print(df)
    for gram in grams[1:]:
        temp_df = data[term][gram]
        norm_series = (df[term] / temp_df[term]).fillna(0)
        df[gram] = (temp_df[gram].multiply(norm_series, axis=0)).round(1)
    return df

def combined_dataframes(terms, min_dist_term, data):
    res = {}
    for term in terms:
        try:
            grams = list(min_dist_term[term].keys())
            res[term] = create_dataframe(term, grams, data)
        except:
            pass
    return res

# print(get_terms_combined())
min_dist_term = get_terms_combined(grams, terms)
res = combined_dataframes(terms, min_dist_term, data)
bg = res["bill gates"] 
vw = res["viruswaarheid"]
sg = res["staatsgreep"]
df_res = pd.DataFrame()
norm1 = (bg["viruswaarheid"] / vw["viruswaarheid"]).fillna(0)
norm2 = (vw["staatsgreep"] / sg["staatsgreep"]).fillna(0)
df_res = bg.join([vw.drop(columns=["viruswaarheid", "date"]).multiply(norm1, axis=0), sg.drop(columns=["staatsgreep", "date"]).multiply(norm2, axis=0).round(1)])
with open("googlesearch/df_rest.csv", "w+") as file:
    df_res.to_csv(file, sep=";", decimal=",")


cat_terms = {}
with open("googlesearch/input/wordsandbigrams.json", "r+") as file:
    temp = json.load(file)
    for k,v in temp["category"].items():
        for l,j in v.items():
            if k not in cat_terms:
                cat_terms[k] = []
            for i in j:
                cat_terms[k].append(i)
df_res_cat = pd.DataFrame(df_res["date"])

for cat, catterms in cat_terms.items():
    df_res_cat[cat]= df_res[catterms].sum(axis=1).round(1)
with open("googlesearch/df_rest_cat.csv", "wb") as file:
    df_res_cat.to_csv(file, sep=";", decimal=",")

with open("LRA/df_trends.json", "w+") as file:
    df_res_cat.to_json(file, indent=4)
    
df_line = df_res_cat.rolling(7).mean()
df_line = df_line.join(df_res_cat["date"])
fig = px.line(df_line, x="date", y=df_line.columns, title='Life expectancy in Canada')
fig.show()