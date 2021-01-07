import pandas as pd
import plotly.express as px

EXCEL_FILE = 'data/Vaccinatiebereidheid.xls'

df = pd.read_excel(EXCEL_FILE, sheet_name='Coded', index_col=0)

print(df)
# print(df.drop(4))

fig = px.line(df, range_y=[0,1]).update_traces(connectgaps=True)

fig.update_layout(
    title="Recorded vaccination willingness per month",
    xaxis_title='Month',
    yaxis_title='Fraction',
    legend_title='Legend',

)
names = {"0": "(Probably) yes", "1": "(Probably) not", "2": "Don't know (yet)"}
fig.show()
