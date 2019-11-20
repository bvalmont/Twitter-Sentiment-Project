import dash
from dash.dependencies import Output, Input
#from dash.dependencies import Event
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
conn_string = "host='localhost' dbname='Twitter Sentiment' user='postgres' password='Joey2016'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

app = dash.Dash(__name__)
app.layout = html.Div(
   [html.H2('Enter Search Term'),
       dcc.Input(id='sentiment_term', value='impeachment', type='text'),
       dcc.Graph(id='live-graph', animate=False
       ),
       dcc.Graph(id='live-graph-geo', animate=False),
       dcc.Interval(
           id='graph-update',
           interval=1*1000
       ),
   ]
)


# def create_table():
#    try:
#        cursor.execute(
#            "CREATE TABLE IF NOT EXISTS tweet_sentiment (id serial primary key, unix bigint, tweet TEXT, coordinates varchar, place varchar, location varchar, username varchar, sentiment decimal)")
#        conn.commit()
#    except Exception as e:
#        print(f"streming twitter error\n{e}")
#
# create_table()


@app.callback(Output('live-graph', 'figure'),
             [Input('sentiment_term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_scatter(sentiment_term, n):
   try:
       df = pd.read_sql("SELECT * FROM tweet_test WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000", conn, params=('%' + sentiment_term + '%',))
       df.sort_values('unix', inplace=True)
       df['date']=pd.to_datetime(df['unix'], unit='ms')
       df.set_index('date', inplace=True)
       df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()

       X = df.index[-100:]
       Y = df['sentiment_smoothed'].values[-100:]

       data = plotly.graph_objs.Scatter(
               x=X,
               y=Y,
               name='Scatter',
               mode='lines+markers'
               )
       return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X),max(X)],title='Date'),
                                                   yaxis=dict(range=[min(Y),max(Y)],title='Sentiment'),
                                                   title='Term: {}'.format(sentiment_term))}
   except Exception as e:
       print(e)
       return {"data": []}


@app.callback(Output('live-graph-geo', 'figure'),
             [Input('sentiment_term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_geo(sentiment_term, n):
    query = "select * from tweet_test WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000"
    df = pd.read_sql(query, conn, params=('%' + sentiment_term + '%',))

    print(df['classification'][-100:])

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
            color=df['classification'].values[-100:]
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