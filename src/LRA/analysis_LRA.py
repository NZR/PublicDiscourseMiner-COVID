"""
Goal: 

Input: 

Output: 

Data extension: (want to do more ?)

"""
import pandas as pd
import json
import statsmodels.api as sm
from statsmodels.formula.api import ols, gls

tweet_file = "df_tweets.json"
google_file = "df_trends.json"
vaccination_file = "willingness.csv"

with open(tweet_file, "r") as file:
    df_tweets = pd.read_json(file)

with open(google_file, "r") as file:
    df_trends = pd.read_json(file)
    df_trends.set_index("date", inplace=True)

with open(vaccination_file, "r") as file:
    df_willing = pd.read_csv(file, sep=";")

df_willing["Date"] = df_willing["Date"].astype("datetime64[ns]")
df_willing.set_index("Date", inplace=True)
df_willing.index = df_willing.index.month

df_trend_month = df_trends.groupby(by=df_trends.index.month).mean().round(1)
df_tweets_month = df_tweets.groupby(by=df_tweets.index.month).sum()

#df_trend_month = a table, for each month, for each category, number of hits. 
#df_twitter_month = a table, for each month, for each cateogry, number of hits

for df in [df_tweets_month, df_trend_month]:
    df_LRA = df.join(df_willing["Willingness"], how="right")
    print(list(df_LRA.columns))
    df_LRA.columns = ["x1", "x2", "x3", "x4", "x5", "x6", "x8", "Willingness"]
    corr_lra = df_LRA.corr()["Willingness"]
    print(corr_lra)
    #Correlation for each category of keywords over the month (based on tweets and trends), with Willingness numbers. 
    largest = list((abs(corr_lra).nlargest(4)[1:]).index)
    model_str = "Willingness ~"
    
    #select / keep the categories with the highest correlation.
    for large in largest:
        model_str += f" {large} +"

    model_str = model_str[:-2]
    model = ols(model_str, data=df_LRA).fit()
    sm.stats.anova_lm(model, typ=2)
    print(model.summary())
    print(model.summary().as_latex())