"""
This file relates to Twitter data sorting. 
It is assumed that the tweeter info is stored into the refined.json file - 
containing structured data (full tweets, with retweets and likes), as well as the categories
that were matched (based on their content). 

The output of this script is the number of tweets emitted on each day that
was found to belong to each category. 

[day 1 - category 1: 12 tweets, category 2: 2 tweets] (a bit like that.)

The output is saved into 2 separated yet identical files
and produces a graph that should open in a separate web browser window.

file 1: df_tweets.json, in the current folder
file 2: df_tweet.json in LRA/ to be used as input for the linear regression analysis.
"""
import json
import dateutil.parser
import pandas as pd
import plotly.express as px


with open("refined.json", "rb") as file:    #load the tweets from the JSON file.
    tweets = json.load(file)

#Recover the categories identified in the previous steps by reading them from the
# df_rest_cat.csv file - that's the only purpose of that block.
with open("../googlesearch/df_rest_cat.csv", "r") as file: 
    shell_df = pd.read_csv(file, sep=";", decimal=",")
    shell_df = shell_df.drop(columns=shell_df.columns[0])
    shell_df.set_index("date", inplace=True)
    df = pd.DataFrame(0, index=shell_df.index, columns=shell_df.columns)
    
cat_terms = list(df.columns)

#"Rearrange the data" -> for individual tweets with categories assigned
# to number of tweet on each day, for each category
for tweet in tweets:
    tweet_date = f"{dateutil.parser.parse(tweet['created_at']):%Y-%m-%d}"
    for cat in cat_terms:
        if cat in tweet["categories"]:
            try:
                df.loc[tweet_date, cat] += 1 # [date, category] -> number of tweet +1
            except KeyError:
                pass

#save the information into 2 different files.
with open("df_tweets.json", "w+") as file:
    df.to_json(file, indent=4)

with open("../LRA/df_tweets.json", "w+") as file:
    df.to_json(file, indent=4)

df_line = df.rolling(7).mean()
fig = px.line(df_line, title='Tweets usage')
fig.show()