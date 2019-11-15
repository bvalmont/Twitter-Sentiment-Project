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

#popular topics: #impeachment, #trump, #quid pro quo
app = dash.Dash(__name__)
app.layout = html.Div(
    [html.H2('Live Twitter Sentiment'),
        dcc.Input(id='sentiment_term', value='impeachment', type='text'),
        dcc.Graph(id='live-graph', animate=True),
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
        conn_string = "host='localhost' dbname='Twitter Sentiment' user='postgres' password='joey2016'"
        conn = psycopg2.connect(conn_string)
        print("CONNECTED WITH CONN")
        #df = pd.read_sql("SELECT sentiment FROM sentiment", conn, params=('%' + sentiment_term + '%',))
        df = pd.read_sql("SELECT * FROM tweet_sentiment WHERE tweet LIKE %s ORDER BY unix DESC LIMIT 1000", conn, params=('%' + sentiment_term + '%',))
        print("PANDAS READ SQL")
        print(df['unix'].values)
        df.sort_values('unix', inplace=True)
        print('SORTING VALUES')
        print(df['unix'])
        df['sentiment_smoothed'] = df['sentiment'].rolling(int(len(df)/5)).mean()
        #df.dropna(inplace=True)
        print('PAST DROPNA')
        print(df['unix'])
        print("DF IS FORMATTED")
        X = df['unix'].values[-100:]
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

        return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[min(X),max(X)]),
                                                    yaxis=dict(range=[min(Y),max(Y)]),
                                                    title='Term: {}'.format(sentiment_term))}
    except Exception as e:
        print(e)
        return {"data": []}


if __name__ == '__main__':
    app.run_server(debug=True)