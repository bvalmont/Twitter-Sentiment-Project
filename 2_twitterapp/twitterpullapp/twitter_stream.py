import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import time
import requests
from keras.models import load_model
import pandas as pd
#import os

analyzer = SentimentIntensityAnalyzer()

#conn_string = "host='####' dbname='####' user='####' password='####'"

conn_string = "host='####' dbname='####' user='####' password='####'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

#dirname = os.path.dirname(__file__)
#filename = os.path.join(dirname, 'static\sentiment_classifier.h5')

#model = load_model(filename)
model = load_model("twitterpullapp/sentiment_classifier.h5")

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# create a dictionary to store your twitter credentials
twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
twitter_cred['CONSUMER_KEY'] = '####'
twitter_cred['CONSUMER_SECRET'] = '####'
twitter_cred['ACCESS_KEY'] = '####'
twitter_cred['ACCESS_SECRET'] = '####'



def classify_sentiment(mdl, sent_metrics_df):
    ml_prediction = mdl.predict(sent_metrics_df)
    if ml_prediction > .5:
        return 2
    else:
        return 1


def create_table():
    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS twitter (id serial primary key, unix bigint, tweet TEXT, coordinates varchar, place varchar, location varchar, username varchar, sentiment decimal, lat float, lng float, classification int)")
        conn.commit()
    except Exception as e:
        print(f"streming twitter error\n{e}")

create_table()


class listener(StreamListener):
    def on_data(self, data):
        all_data = json.loads(data)
        tweet = all_data["text"].replace("'", "''")

        try:
            print(all_data["coordinates"])
            coordinates = all_data["coordinates"]
        except:
            coordinates = "NA"

        try:
            print(all_data["place"])
            place = all_data["place"]["full_name"]
        except:
            place = all_data["place"]

        try:
            location = all_data["user"]["location"].replace("'", "''")
        except:
            location = all_data["user"]["location"]

        username = all_data["user"]["screen_name"]
        # Get the Sentiment score of the tweet

        tweet_time = all_data['timestamp_ms']

        # Google developer API key
        #gkey = "####"



        # Target city
        #target_city = all_data["user"]["location"]

        try:
            target_city = all_data["user"]["location"].split(",")[0]
            print(target_city)
        except:
            target_city = "NaN"




        # Build the endpoint URL
        #target_url = ('https://maps.googleapis.com/maps/api/geocode/json?'
        #              'address={0}&key={1}').format(target_city, gkey)

        target_url = 'https://gist.githubusercontent.com/Miserlou/c5cd8364bf9b2420bb29/raw/2bf258763cdddd704f8ffd3ea9a3e81d25e2c6f6/cities.json'              

        # Run a request to endpoint and convert result to json
        try:
            geo_data = requests.get(target_url).json()
            

        # Print the json
        except:
            geo_data = "NaN"

        # Extract latitude and longitude
        if geo_data == 'NaN':
            lat = 0
            lng = 0
        else:
            try:
                lat = 0
                lng = 0
                #lat = geo_data["results"][0]["geometry"]["location"]["lat"]
                #lng = geo_data["results"][0]["geometry"]["location"]["lng"]
                for i in range(0, 1000):
                    if geo_data[i]["city"] == target_city:
                        lat = lat + geo_data[i]["latitude"]
                        lng = lng + geo_data[i]["longitude"]
                        print(lat)
                        print(lng)

            except:
                lat = 0
                lng = 0

        vs = analyzer.polarity_scores(tweet)
        sentiment = vs['compound']
        neg = vs['neg']
        pos = vs['pos']
        neu = vs['neu']

        sent_metrics_df = pd.DataFrame([[neg, pos, neu, sentiment]])

        sent_classification = classify_sentiment(model, sent_metrics_df)

        cursor.execute(
            "Insert into twitter (unix, tweet, coordinates, place, location, username, sentiment, lat, lng, classification) Values "
            "(%s, '%s', '%s', '%s', '%s', '%s', '%s' , '%f', %f, '%i');" %
            (tweet_time, tweet, coordinates, place, location, username, sentiment, lat, lng, sent_classification))
        conn.commit()

        print(tweet, sentiment)
        print(coordinates, place, location, username)
        return True

    def on_error(self, status):
        print(status)


while True:

    try:
        key_words = ["impeachment"]
        print("ONE")
        auth = OAuthHandler(twitter_cred['CONSUMER_KEY'], twitter_cred['CONSUMER_SECRET'])
        print("TWO")
        auth.set_access_token(twitter_cred['ACCESS_KEY'], twitter_cred['ACCESS_SECRET'])
        print("THREE")
        twitterStream = Stream(auth, listener(), tweet_mode='extended')
        print("FOUR")
        twitterStream.filter(track=key_words, languages=['en'])
        print("FIVE")
        time.sleep(1)
    except Exception as e:
        print(f"streming steelers error\n{e}")
        time.sleep(5)