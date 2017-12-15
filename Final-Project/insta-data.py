#This code requests data from Instagram API, saves raw data into cache, and saves relevant data points into database

import requests
import json
import insta_token
import sqlite3

base_url='https://api.instagram.com/v1/users/'

try:
	access_token=insta_token.access_token #Imports my instagram access token
except: 
	access_token=input('Please enter access token from https://www.instagram.com/developer/:\n\n')

cache_fname='insta-data.json'

try: #Initializes cache
	cache_file=open(cache_fname, 'r')
	cache_contents=cache_file.read()
	cache_diction=json.loads(cache_contents)

except:
	cache_diction={}

def get_data(user_id):
	
	if user_id in cache_diction: #If user data in cache, uses cache data
		print ('Using cached data\n\n')
		post_data=cache_diction[user_id]
	
	else: #If not in cache, requests data from Instagram API
		print ('Fetching data from Instagram\n\n')
		
		r=requests.get(base_url+user_id+'/media/recent?access_token='+access_token)
		post_data=r.text
		cache_diction[user_id]=post_data #Writes data to cache
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_diction))
		cache_writer.close()
		
		print ('Raw Instagram Data Has Been Saved To The Cache File insta-data.py\n\n')
	
	return (post_data)

user_id=input('Enter the user id of whoever you want to get post data from.  Leave blank for yourself: \n\n') #Users with valid permissions can search posts from any user or themselves
if len(user_id)<1:
	user_id='self'

insta_posts=json.loads(get_data(user_id)) #Calls function to get Instagram data

conn=conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

cur.execute('DROP TABLE if EXISTS Instagram') #Creates database table for Instagram data
cur.execute('Drop Table if exists Posts')
cur.execute('''Create Table Instagram (id Integer Primary Key AutoIncrement,name Varchar, caption Varchar, likes Integer, time_posted Timestamp, latitude Varchar, longitude Varcahar, weather Varchar)''')

post_data=insta_posts['data']

for post in post_data: #Extracts relevant data points from raw data
	name=post['user']['full_name']
	caption=post['caption']['text']
	likes=post['likes']['count'] 
	time=post['created_time']
	
	try: #Tries to get geodata from posts
		latitude=str(post['location']['latitude'])
		longitude=str(post['location']['longitude'])
	
	except:
		latitude=''
		longitude=''
	
	tup=(name, caption, likes, time, latitude, longitude) #Creates tuple to write rows into table
	
	cur.execute('Insert into Instagram (name, caption, likes, time_posted, latitude, longitude) values (?,?,?,?,?,?)', tup)

conn.commit()
cur.close()

print ('Relevant Instagram Data Has Been Saved In The Table Instagram In The Database 206-Final.sqlite\n\n')










