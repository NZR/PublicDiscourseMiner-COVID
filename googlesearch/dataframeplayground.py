import json
import pandas as pd
import time
import sys
from io import StringIO

INFILE = "./output/staatsgreepcorona.json"
normalisation_terms = ['viruswaarheid']


def create_dataframe(normalisation_term, data):
    dataframe = pd.DataFrame()
    first_iteration = True
    for term in list(data[normalisation_term].keys()):
        temp_dataframe = pd.read_csv(data[normalisation_term][term])
        print(temp_dataframe)


# parse csv

# read (converted) csv for this all terms compared to this term

# scale value to term X

# insert column in dataframe

# return dataframe


# Open json
with open(INFILE) as json_file:
    data = json.load(json_file)
    print(data['viruswaarheid']['bill'])
    print(pd.read_csv(StringIO(data['viruswaarheid']['bill']), sep=';'))

    dataframe = pd.DataFrame()
    temp_dataframe = pd.read_csv(StringIO(data['viruswaarheid']['bill']), sep=';')
    dataframe['date'] = temp_dataframe['date']

    # copy normalisation term
    dataframe['viruswaarheid'] = temp_dataframe['viruswaarheid']

    # copy dataterm
    term_vals = temp_dataframe['bill'].tolist()
    normalisation_term_vals = dataframe['viruswaarheid'].tolist()
    for i in range(len(term_vals)):
        term_vals[i] = term_vals[i] + normalisation_term_vals[i]
    dataframe['bill'] = term_vals
    print(dataframe)



