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

analyzer = SentimentIntensityAnalyzer()

conn_string = "host='localhost' dbname='Twitter Sentiment' user='postgres' password='Joey2016'"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()

model = load_model(r'C:\Users\asia8_000\Desktop\z.Temp\Rice_Data_Analytics_Boot_Camp\005 - Project.3\deep-state-github\Twitter-Sentiment-Project\dev_code\sentiment_classifier.h5')
model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# create a dictionary to store your twitter credentials
twitter_cred = dict()

# Enter your own consumer_key, consumer_secret, access_key and access_secret
twitter_cred['CONSUMER_KEY'] = 'iq4AzDBihRqrrrHiUR4QLteq3'
twitter_cred['CONSUMER_SECRET'] = '6j2fP4YuxdA5Qdukqc43llrAqiKg7bTKQV8F9ZBIBNFF8ARNng'
twitter_cred['ACCESS_KEY'] = '851628439-1DZOydLYSLvjPoxIRXxiQ3VUTLYkdxXHqRhngAKu'
twitter_cred['ACCESS_SECRET'] = '6psI4BVfZutxTUXwV6vroZG23cuaOFbziCVfsmRhuWkTS'

# Save the information to a json so that it can be reused in code without exposing
# the secret info to public
with open('twitter_credentials.json', 'w') as secret_info:
    json.dump(twitter_cred, secret_info, indent=4, sort_keys=True)
# load Twitter API credentials
with open('twitter_credentials.json') as cred_data:
    info = json.load(cred_data)
    consumer_key = info['CONSUMER_KEY']
    consumer_secret = info['CONSUMER_SECRET']
    access_key = info['ACCESS_KEY']
    access_secret = info['ACCESS_SECRET']


def classify_sentiment(mdl, sent_metrics_df):
    ml_prediction = mdl.predict(sent_metrics_df)
    if ml_prediction > .5:
        return 2
    else:
        return 1


def create_table():
    try:
        cursor.execute(
            "CREATE TABLE IF NOT EXISTS tweet_test (id serial primary key, unix bigint, tweet TEXT, coordinates varchar, place varchar, location varchar, username varchar, sentiment decimal, lat float, lng float, classification int)")
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
        gkey = "AIzaSyD8z3OVuovAThyZuyou290-wm4qbNERFvk"

        # Target city
        target_city = all_data["user"]["location"]

        # Build the endpoint URL
        target_url = ('https://maps.googleapis.com/maps/api/geocode/json?'
                      'address={0}&key={1}').format(target_city, gkey)

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
                lat = geo_data["results"][0]["geometry"]["location"]["lat"]
                lng = geo_data["results"][0]["geometry"]["location"]["lng"]
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
            "Insert into tweet_test (unix, tweet, coordinates, place, location, username, sentiment, lat, lng, classification) Values "
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
        auth = OAuthHandler(consumer_key, consumer_secret)
        print("TWO")
        auth.set_access_token(access_key, access_secret)
        print("THREE")
        twitterStream = Stream(auth, listener(), tweet_mode='extended')
        print("FOUR")
        twitterStream.filter(track=key_words, languages=['en'])
        print("FIVE")
        time.sleep(1)
    except Exception as e:
        print(f"streming steelers error\n{e}")
        time.sleep(5)