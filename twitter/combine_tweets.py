import json
import dateutil.parser
import pandas as pd
import plotly.express as px


with open("twitter/refined.json", "rb") as file:
    tweets = json.load(file)

# print(tweets)
# print(tweets.__class__)



with open("df_rest_cat.csv", "r") as file:
    shell_df = pd.read_csv(file, sep=";", decimal=",")
    shell_df = shell_df.drop(columns=shell_df.columns[0])
    shell_df.set_index("date", inplace=True)
    df = pd.DataFrame(0, index=shell_df.index, columns=shell_df.columns)
    
cat_terms = list(df.columns)
for tweet in tweets:
    tweet_date = f"{dateutil.parser.parse(tweet['created_at']):%Y-%m-%d}"
    for cat in cat_terms:
        if cat in tweet["categories"]:
            try:
                df.loc[tweet_date, cat] += 1
            except KeyError:
                pass

df_line = df.rolling(7).mean()
fig = px.line(df_line, title='Tweets usage')
fig.show()