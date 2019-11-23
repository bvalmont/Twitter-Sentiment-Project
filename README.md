# Project 3 | Twitter Sentiment Analysis

Ren Galindo | Richard Harris | Daniel Jones | Brandon Valmont

## Background

Team Deep-State was tasked with using Machine Learning to solve a problem worth solving, analyzing, and visualizing.  The team decided to perform a sentiment analysis on Twitter tweets pertaining to the Impeachment of President Donald Trump.  To perform this analysis, we had to create code to live stream tweets on the selected topic, load the data into Postgres database, run the data through our sentiment testing, which identified the tweets as positive or negative, and visualize the live results on a line graph and plotting the locations of the tweets on a map.

![alt text](https://github.com/bvalmont/Twitter-Sentiment-Project/blob/master/Images/man-person-people-emotions-1.jpg)

## Technology

In order for us to complete this request, we utilized:
   - Python
   - Jupyter NoteBooks
   - Visual Studio Code
   - Postgres
   - Tweepy - Python library for accessing the Twitter API
   - Google Maps API
   - Plotly Dash for visualizations
   - Vader Sentiment - VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media
   - Heroku

## Data Sources 
  - **Twitter** - ( https://www.twitter.com ) 
  - Twitter Streaming API - a push of data as tweets happen in near real-time
  
## Project Design
![alt text](https://github.com/bvalmont/Twitter-Sentiment-Project/blob/master/Images/overview-page.png)
- Data Collection

As stated in the background, the purpose of the project was to perform a sentiment analysis on twitter data related to the impeachment of President Donald Trump.  The first step in the process is collecting tweets in real-time from Twitter.  In order to do this, we imported Tweepy, a python library for accessing the Twitter Streaming API.  Using the Twitter Streaming API, users can expect to receive anywhere from 1% of the tweets to over 40% of the tweets in near real-time.  One tweet can produce up to 150 attributes; therefore, for this project we only collected data on five of the attributes: text, coordinates, place, location, and screen name.
The next step in the process was to load the data in the Postgres database; however, we found that vast majority of the "coordinates" were not populated.  One of the objectives of the project was to have a map with real-time plots displaying the location of the tweets, which requires the geo information.  Since the locations for most of the tweets were populated, we created code using the Google Map API which produced the latitude and longitude for the "locations" associated with each tweet.  As a result, we would need to add two additional fields to our database.  

- Sentiment Analysis

Prior to loading the data into Postgres, we needed to determine whether the tweets were positive, neutral, or negative. For the sentiment analysis, we used VADER sentiment.  VADER (Valence Aware Dictionary and sEntiment Reasoner) is a lexicon and rule-based sentiment analysis tool that is specifically attuned to sentiments expressed in social media.  VADER combines a dictionary, which maps lexical features to emotion intensity, and five simple heuristics, which encode how contextual elements increment, decrement, or negate the the sentiment of text.  The power of the lexical approach lies in the fact that we do not need to train a model using labeled data, since we have everything we need to assess the sentiment of sentences in the dictionary of emotions. VADER returns a sentiment score in the range -1 to 1,from most negative to most positive.  The sentiment score of a sentence is calculated by summing up the sentiment scores of each VADER dictionary-listed word in the sentence.  Individual words have a sentiment score between -4 to 4, but normalization is applied to the total to convert it to a value between -1 and 1.

- Machine Learning

Since VADER sentiment is a dictionary words that cannot be trained, we built a machine learning model that would result in positive/negative scores based on the VADER metrics.  We trained our model on 90% of 10,662 rows of movie review data, which were given scores from VADER.  VADER results in four unique metrics: positive, neutral, negative, and compound.  The model when trained converts/predicts a sentiment score between 1 and 2 based on what it learned from the movie reviews.  A score higher than 0.5 is classified as positive returns a score of 2, a score less than 0.5 is classified as negative returns a score of 1, and a score of 0.5 is considered neutral.  Next, we processed the streaming tweets through the model, which get classified into one of the three categories, and then plotted on the map at the location of the tweet while being categorized as red or blue for being positive or negative.

- Database Load

The next step in the process was to load the data in the PostgreSQL database.  Python and the psycopg2 library were utilized to connect to a cloud based version of PostgreSQL since the app would be deployed to a production server.  The PostgreSQL table serving the app would need to have columns representing the data being steamed from Twitter.  In this case the most important columns for the app were location, in the format of Here, TX which was converted to lat and lng columns.  The tweet column contained actual tweets of twitter users which the machine learning utilized to assign a sentiment score which was also a seperate column.  The columns mentioned in the table would be used to create visualizations such as a real-time sentiment analysis graph and a map of the United States that visualizes the location of the twitter user along with a color of red or blue for the score.
  
- Visualizations

Next, we created a live-updating graph of Twitter sentiment for a term we choose, in this case 'impeachment'. To accomplish this we utilized a live graph created with Dash and Python. Dash is a productive Python framework for building web applications. Dash is written on top of Flask and Plotly.js. Our Dash app is viewed in the web browser and shared through a URL. 
The Dash app is composed of two parts. The first part is the "layout" of the app and it describes what the application looks like. The second part describes the interactivity of the application.  On the graph we replaced the X and Y varibles with our data from our PostgreSQL database. The X axis is Interval graph update set to 1 second. The Y axis is set to the assigned sentiment score of the tweet converted to a value between -1 and 1.  To be streaming live, we needed to have a program also running with the twitter API credentials filled out. Once we run, the Sentiment Line Chart is generated displaying the live tweet scores updating each second. 

The second visualiation created is a Geo Locations of Tweets map.  The geo map shows live sentiment scores of tweets related to the word 'impeachment'. 'Red' dots indicate negative sentiment. 'Blue' dots indicate positive sentiment.  
New search terms entered into the search term box will result in a sub-population of the original population of tweets filtered|pulled on the term 'impeachment'.

## Visualizations

## *Sentiment Line Chart*
![alt text](https://github.com/bvalmont/Twitter-Sentiment-Project/blob/master/Images/sentiment_stream.PNG)

## *Tweet Location Map*
![alt text](https://github.com/bvalmont/Twitter-Sentiment-Project/blob/master/Images/geo_tweets.PNG)
 
## Submission

https://deep-state.herokuapp.com/


© 2019 Deep-State | Ren Galindo - Richard Harris - Daniel Jones - Brandon Valmont | Twitter Whisperers
