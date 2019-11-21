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
   
- Load

   


## Visualizations
 
## Submission







© 2019 Deep-State | Ren Galindo - Richard Harris - Daniel Jones - Brandon Valmont | Twitter Whisperers
