import matplotlib.pyplot as plt
import json
import pandas as pd

with open("output/bill_gates2.json") as json_file:
    jsonfile = json.load(json_file)

keys = list(jsonfile['bill gates'].keys())
vals = list(jsonfile['bill gates'].values())
plt.plot(keys, vals)
plt.show()
