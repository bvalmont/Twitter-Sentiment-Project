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
![alt text](https://github.com/bvalmont/Twitter-Sentiment-Project/blob/master/Images/Overview-pg.png)
- Data Collection

   As stated in the background, the purpose of the project was to perform a sentiment analysis on twitter data related to the impeachment of President Donald Trump.  The first step in the process is collecting tweets in real-time from Twitter.  In order to do this, we imported Tweepy, a python library for accessing the Twitter Streaming API.  Using the Twitter Streaming API, users can expect to receive anywhere from 1% of the tweets to over 40% of the tweets in near real-time.  One tweet can produce up to 150 attributes; therefore, for this project we only collected data on five of the attributes: text, coordinates, place, location, and screen name.
The next step in the process was to load the data in the Postgres database; however, we found that vast majority of the "coordinates" were not populated.  One of the objectives of the project was to have a map with real-time plots displaying the location of the tweets, which requires the geo information.  Since the locations for most of the tweets were populated, we created code using the Google Map API which produced the latitude and longitude for the "locations" associated with each tweet.  As a result, we would need to add two additional fields to our database.

- Sentiment Analysis

- Load

The next step in the process was to load the data in the PostgreSQL database.  Python and the psycopg2 library were utilized to connect to a cloud based version of PostgreSQL since the app would be deployed to a production server.  The PostgreSQL table serving the app would need to have columns representing the data being steamed from Twitter.  In this case the most important columns for the app were location, in the format of Here, TX which was converted to lat and lng columns.  The tweet column contained actual tweets of twitter users which the machine learning utilized to assign a sentiment score which was also a seperate column.  The columns mentioned in the table would be used to create visualizations such as a real-time sentiment analysis graph and a map of the United States that visuzlizes the location of the twitter user along with a color of red or blue for the score.
   


## Visualizations
 
## Submission







© 2019 Deep-State | Ren Galindo - Richard Harris - Daniel Jones - Brandon Valmont | Twitter Whisperers
