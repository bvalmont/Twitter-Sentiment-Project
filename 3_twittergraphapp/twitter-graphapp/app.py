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
app.title="twitter-graphapp"



app.layout = html.Div(
   [html.H2('Enter Search Term'),
       dcc.Input(id='sentiment_term', value='impeachment', type='text'),
       dcc.Graph(id='live-graph', animate=False
       ),

       dcc.Interval(
           id='graph-update',
           interval=1*1000
       ),
   ]
)


@app.callback(Output('live-graph', 'figure'),
             [Input('sentiment_term', 'value'), Input('graph-update', 'n_intervals')])
def update_graph_scatter(sentiment_term, n):
   try:
       df = pd.read_sql("SELECT * FROM twitter WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000", conn, params=('%' + sentiment_term + '%',))
       df.sort_values('unix', inplace=True)
       df['date']=pd.to_datetime(df['unix'], unit='ms')
       df.set_index('date', inplace=True)
       df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()

       print(df['classification'].head(10))

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


if __name__ == '__main__':
   app.run_server(debug=True)


