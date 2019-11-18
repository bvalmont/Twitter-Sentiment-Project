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
conn_string = "host='localhost' dbname='Twitter Sentiment' user='postgres' password='Alicia.30'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
def create_table():
   try:
       cursor.execute(
           "CREATE TABLE IF NOT EXISTS tweet_sentiment (id serial primary key, unix bigint, tweet TEXT, coordinates varchar, place varchar, location varchar, username varchar, sentiment decimal)")
       conn.commit()
   except Exception as e:
       print(f"streming twitter error\n{e}")
create_table()
#popular topics: #impeachment, #trump, #quid pro quo
app = dash.Dash(__name__)
app.layout = html.Div(
   [html.H2('Enter Search Term'),
       dcc.Input(id='sentiment_term', value='impeachment', type='text'),
       dcc.Graph(id='live-graph', animate=False,figure={               
               "layout": {
                    "title" : {
                        'text': 'Basic non interpractive'
                    },
                    'xaxis' : {
                        'title' : {
                            "text":'SP'
                            }
                    },
                    'yaxis' : {
                        'title' : {
                            "text": 'Number of issues'
                            }
                    }
          }
       }
       
       ),
       dcc.Interval(
           id='graph-update',
           interval=1*1000
       ),
   ]
)
#events=[Event('graph-update', 'interval')]
@app.callback(Output('live-graph', 'figure'),
             [Input('sentiment_term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_scatter(sentiment_term, n):
   try:
       #conn_string2 = "host='localhost' dbname='Twitter Sentiment' user='postgres' password='joey2016'"
       #conn2 = psycopg2.connect(conn_string2)
       #print("CONNECTED WITH CONN")
       #df = pd.read_sql("SELECT sentiment FROM sentiment", conn, params=('%' + sentiment_term + '%',))
       df = pd.read_sql("SELECT * FROM tweet_sentiment WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000", conn, params=('%' + sentiment_term + '%',))
       print("PANDAS READ SQL")
       print(df['unix'].values)
       df.sort_values('unix', inplace=True)
       df['date']=pd.to_datetime(df['unix'], unit='ms')
       df.set_index('date', inplace=True)
       print('SORTING VALUES')
       print(df['unix'])
       df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
       #df.dropna(inplace=True)
       # df = df.resample('5s').mean()
       print('PAST DROPNA')
       print(df['unix'])
       print("DF IS FORMATTED")
       X = df.index[-100:]
       print("XXXXXXXXX")
       print(X)
       Y = df['sentiment_smoothed'].values[-100:]
       print("YYYYYYYYY")
       print(Y)
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
if __name__ == '__main__':
   app.run_server(debug=True)

