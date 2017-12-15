#This code get data from the Facebook API, saves raw data to cache file, and saves relevant data points into database

import requests
import facebook
import json
import sqlite3

cache_fname='fb-data.json'
access_token=input('Please enter access key from https://developers.facebook.com/tools/explorer/:\n\n')
#Needs access token with permission for user_posts

try: #Initializes cache
	cache=open(cache_fname, 'r')
	cache_data=cache.read()
	cache_dict=json.loads(cache_data)
	cache.close()

except:
	cache_dict={}

def get_fb_data(user_id, access_token):
	
	if user_id in cache_dict.keys(): #If Facebook data in cache, uses cached data
		print ('Using Cached Facebook Data\n\n')
		post_data=cache_dict[user_id]
	
	else: #If data not in cache, makes request to Facebook API
		print ('Fetching Data From Facebook\n\n')
		
		post_data=[]

		base_url='https://graph.facebook.com/v2.10/'+user_id+'/feed/' #Gets data from user feed
		
		url_params={} #Initializes dictionary for request parameters
		url_params['fields']='from, message, type, likes.summary(true), created_time, place' #Data to get for each post		
		url_params['access_token']=access_token
		r=requests.get(base_url,params=url_params)
		
		posts=r.text
		posts_dict=json.loads(posts)
		
		for post in posts_dict['data']:
			if 'likes' and 'message' in post: #Only saves posts that have data about likes and message
				post_data.append(post)

		while 'paging' in posts_dict: #Goes through paged results to get data for all posts
			r=requests.get(posts_dict['paging']['next'])
			posts=r.text
			posts_dict=json.loads(posts)
			
			for post in posts_dict['data']:
				
				if 'likes' and 'message' in post: #Only saves posts that have data about likes and message
					post_data.append(post)
		
		post_data=json.dumps(post_data)	#Writes data into cache		
		cache_dict[user_id]=post_data
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_dict, indent=4))
		cache_writer.close()

		print ('Raw Facebook Data Has Been Saved To The Cache File fb-data.json\n\n')
	
	return (post_data)

user_id=input('Enter user id of whoever you want to get data from.  Leave blank for yourself: \n') #Users with valid permissions can get data for any user, or themselves
if len(user_id)<1:
	user_id='me'

post_data=json.loads(get_fb_data(user_id, access_token)) #Calls function to get Facebok data
popular_posts=sorted(post_data, key=lambda x:x['likes']['summary']['total_count'], reverse=True)[:100] #Sorts posts by number of likes and returns 100 most popular posts

conn=conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

cur.execute('Drop Table if Exists Facebook') #Creates database table to store relevant Facebook data points
cur.execute('Create Table Facebook (id Integer Primary Key Autoincrement, name Varchar, type Varchar, message Varchar, likes Integer, time_posted Timestamp, latitude Varchar, longitude Varchar, weather Varchar)')

for post in popular_posts: #Extracts relevant data points from raw Facebook data
	name=post['from']['name']
	typ=post['type']
	message=post['message']
	likes=post['likes']['summary']['total_count']
	time_posted=post['created_time'][:-5]
	
	try: #Tries to extract geodata from posts
		latitude=str(post['place']['location']['latitude'])
		longitude=str(post['place']['location']['longitude'])
	
	except:
		latitude=''
		longitude=''

	tup=(name, typ, message, likes, time_posted, latitude, longitude) #Creates tuple to write into database

	cur.execute('Insert into Facebook (name, type, message, likes, time_posted, latitude, longitude) values (?,?,?,?,?,?,?)', tup)
	conn.commit()

cur.close()

print ('Relevant Facebook Data Has Been Saved Into The Table Facebook In The Database 206-Final.sqlite\n\n')



