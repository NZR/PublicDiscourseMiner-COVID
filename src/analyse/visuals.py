import plotly
from database.connector import Connector

db = Connector()
# Column names are: datum, auteur, link, themes, triggers, bigrams, full_without_stop, full_text, nepnieuws
# real_dates = db.select()
dates = db.select("datum")
print(dates)