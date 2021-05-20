import json
import pandas as pd
from io import StringIO


INFILE = "./output/staatsgreepcorona.json"
normalisation_terms = ['viruswaarheid']


def create_dataframe(normalisation_term, data):
    dataframe = pd.DataFrame()
    first_iteration = True
    for term in list(data[normalisation_term].keys()):
        temp_dataframe = pd.read_csv(StringIO(data[normalisation_term][term]), sep=';')
        if not first_iteration:
            # only fetch column of term divided by normalisation term
            term_vals = temp_dataframe[term].tolist()
            normalisation_term_vals = dataframe[normalisation_term].tolist()
            for i in range(len(term_vals)):
                term_vals[i] = term_vals[i] / normalisation_term_vals[i]
            dataframe[term] = term_vals
        else:
            # copy data
            dataframe['date'] = temp_dataframe['date']
            # copy normalisation term
            dataframe[normalisation_term] = temp_dataframe[normalisation_term]
            # copy dataterm
            term_vals=temp_dataframe[term].tolist()
            normalisation_term_vals = dataframe[normalisation_term].tolist()
            for i in range(len(term_vals)):
                term_vals[i] = term_vals[i] / normalisation_term_vals[i]
            dataframe[term] = term_vals
            first_iteration = False

    return dataframe


# Open json
with open(INFILE) as json_file:
    data = json.load(json_file)
    for normalisation_term in normalisation_terms:
        create_dataframe(normalisation_term, data)






