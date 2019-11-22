import json
import pandas as pd
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import psycopg2
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time


analyzer = SentimentIntensityAnalyzer()

conn_string = "host='localhost' dbname='Twitter Sentiment' user='postgres' password='password'"
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
        vs = analyzer.polarity_scores(tweet)
        sentiment = vs['compound']

        tweet_time = all_data['timestamp_ms']

        cursor = conn.cursor()
        cursor.execute("Insert into tweet_sentiment (unix, tweet, coordinates, place, location, username, sentiment) Values "
                       "(%s, '%s', '%s', '%s', '%s', '%s', %s);" %
                       (tweet_time, tweet, coordinates, place, location, username, sentiment))
        conn.commit()

        print(tweet, sentiment)
        print(coordinates, place, location, username)
        return (True)

    def on_error(self, status):
        print(status)


while True:

    try:
        key_words = ["trump","donald trump", "president","impeachment"]
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
