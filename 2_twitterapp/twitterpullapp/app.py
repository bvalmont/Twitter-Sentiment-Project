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
from .twitter_stream import *

analyzer = SentimentIntensityAnalyzer()

conn_string = "host='#####' dbname='#####' user='#####' password='#####'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()



app = dash.Dash(__name__)
server = app.server
app.title="twitterpullapp"





if __name__ == '__main__':
   app.run_server(debug=True)


