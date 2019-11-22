import dash
from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import sqlalchemy
import pandas as pd
import time
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


analyzer = SentimentIntensityAnalyzer()
conn_string = "host='####' dbname='####' user='####' password='####'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()


app = dash.Dash(__name__)
server = app.server
app.title="twitter-mapapp"



app.layout = html.Div(
   [html.H2('Enter Search Term'),
       dcc.Input(id='sentiment_term', value='impeachment', type='text'),
       #dcc.Graph(id='live-graph', animate=False),
       dcc.Graph(id='live-graph-geo', animate=False),
       dcc.Interval(
           id='graph-update',
           interval=1*1000
       ),
   ]
)



@app.callback(Output('live-graph-geo', 'figure'),
             [Input('sentiment_term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_geo(sentiment_term, n):
    query = "select * from twitter WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000"
    df = pd.read_sql(query, conn, params=('%' + sentiment_term + '%',))

    #print(df['classification'][-100:])

    data = [ dict(
        type = 'scattergeo',
        locationmode = 'USA-states',
        lon = df['lng'].values[-100:],
        lat = df['lat'].values[-100:], #change to lng
        text = df['location'].values[-100:],
        mode = 'markers',
        marker = dict(
            size = 8,
            opacity = 0.8,
            reversescale = False,
            autocolorscale = False,
            symbol = 'circle',
            line = dict(
                width=1,
                color='rgb(0, 0, 0)'
                
            ),
            colorscale="ReBl",
            color = df['classification'].values[-100:]
        ))]

    return {'data': data, 'layout': go.Layout(title='Geo Locations of Tweets<br>(Hover for Location Names)',
                                                geo = dict(
                                                    scope='usa',
                                                    projection=dict( type='albers usa' ),
                                                    showland = True,
                                                # landcolor = "rgb(250, 250, 250)",
                                                # subunitcolor = "rgb(217, 217, 217)",
                                                # countrycolor = "rgb(217, 217, 217)",
                                                    countrywidth = 0.5,
                                                    subunitwidth = 0.5
                                                ))}



if __name__ == '__main__':
   app.run_server(debug=True)


