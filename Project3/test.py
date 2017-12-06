import unittest
import itertools
import collections
import tweepy
import twitter_info
import json
import sqlite3

## Your name: Alex Kahan
## The names of anyone you worked with on this project:

#####

##### TWEEPY SETUP CODE:
# Authentication information should be in a twitter_info file...
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Set up library to grab stuff from twitter with your authentication, and 
# return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

##### END TWEEPY SETUP CODE

## Task 1 - Gathering data

## Define a function called get_user_tweets that gets at least 20 Tweets 
## from a specific Twitter user's timeline, and uses caching. The function 
## should return a Python object representing the data that was retrieved 
## from Twitter. (This may sound familiar...) We have provided a 
## CACHE_FNAME variable for you for the cache file name, but you must 
## write the rest of the code in this file.

CACHE_FNAME = "206_APIsAndDBs_cache.json"
# Put the rest of your caching setup here:
try:
	cache=open(CACHE_FNAME,'r')
	cache_contents=cache.read()
	cache_dict=json.loads(cache_contents)
	cache.close()
except:
	cache_dict={}

# Define your function get_user_tweets here:
def get_user_tweets(keyword):
	if keyword in cache_dict:
		print ('Using Cached Data')
		tweets=cache_dict[keyword]
	else:
		print ('Fetching data from Twitter')
		tweets=api.user_timeline(keyword)
		cache_dict[keyword]=tweets
		cache_writer=open(CACHE_FNAME, 'w')
		cache_writer.write(json.dumps(cache_dict))
		cache_writer.close()
	return (tweets)



# Write an invocation to the function for the "umich" user timeline and 
# save the result in a variable called umich_tweets:
keyword=input('Enter user you would like to retrieve tweets from: ')
if len(keyword)<1:
	keyword='umsi'
umich_tweets=get_user_tweets(keyword)


conn=sqlite3.connect('206_APIsAndDBs.sqlite')
cur=conn.cursor()

cur.execute('DROP Table if Exists Users')
cur.execute('DROP Table if Exists Tweets')
cur.execute('''Create Table Users (user_id TEXT PRIMARY KEY UNIQUE, screenname VARCHAR, num_favs INTEGER, description VARCHAR)''')

cur.execute('''Create Table Tweets(tweet_id TEXT PRIMARY KEY UNIQUE, text VARCHAR, user_posted TEXT, time_posted TIMESTAMP, retweets INTEGER)''')

for tweet in umich_tweets:
	tup=(tweet['id_str'], tweet['text'],tweet['user']['id_str'] ,tweet['created_at'], tweet['retweet_count'])
	cur.execute('Insert into Tweets (tweet_id, text, user_posted, time_posted, retweets) Values (?,?,?,?,?)', tup,)
conn.commit()

user_dict={}

for tweet in umich_tweets:
	user=api.get_user(tweet['user']['screen_name'])
	if user['name'] not in user_dict:
		user_dict[user['name']]=user
	for person in tweet['entities']['user_mentions']:
		user=api.get_user(person['screen_name'])
		if user['name'] not in user_dict:
			user_dict[user['name']]=user

for user in user_dict.keys():
	tup=(user_dict[user]['id_str'], user_dict[user]['screen_name'], user_dict[user]['favourites_count'], user_dict[user]['description'])
	cur.execute('Insert into Users (user_id, screenname, num_favs, description) Values (?,?,?,?)', tup,)

conn.commit()
screen_names = []
rows=cur.execute('SELECT (screenname) FROM USERS')
for row in rows:
	print (type(row[0]))
	screen_names.append(row[0])

	
cur.close()
	