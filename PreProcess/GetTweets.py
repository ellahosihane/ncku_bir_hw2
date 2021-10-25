import os
import tweepy
import json
from tqdm import tqdm
import os
import datetime

path = os.getcwd()

consumer_key= 'mCbUZtJ0GsY4HbJiriO1fqMsr'
consumer_secret= 'e2CjKWVEvqqLJVL5wphc8Nv3ZE6nCBROedOmfNScCnNdYF0fhQ'
access_token= '2255919739-ETc5DMA05X8MiGSbMvRp2lTjzfBy5EMgs4U8i78'
access_token_secret= 'D9P57a9LiTfOOY8wj1B1C9qbpqj9UnTZPOHJKmbFFCXOX'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=False)

search_words = ["#covid19", "#covid"]
date_since = "2021-01-01"
date_end = "2021-06-01"

tweets = tweepy.Cursor(api.search_tweets,
                       q=search_words,
                       lang="en",
                       since=date_since, 
                       until=date_end).items(1000)
                       
tweet_data = []
for tweet in tweets:
    data = {}
    data["name"] = tweet.user.name
    data["screen_name"] = tweet.user.screen_name
    data["text"] = tweet.text
    tweet_data.append(data)

print(len(tweet_data))    
with open (f'{path}/data0_1000.json','w') as fjson:
    json.dump(tweet_data, fjson)