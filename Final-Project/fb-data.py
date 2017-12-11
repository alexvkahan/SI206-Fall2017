import requests
import facebook
import json
import fb_info
import sqlite3

cache_fname='fb-data.json'

try:
	cache=open(cache_fname, 'r')
	cache_data=cache.read()
	cache_dict=json.loads(cache_data)
	cache.close()

except:
	cache_dict={}

def get_fb_data(user_id, access_token):
	
	if user_id in cache_dict.keys():
		print ('Using Cached Data')
		post_data=cache_dict[user_id]
	
	else:
		print ('Fetching data from Facebook')
		
		post_data=[]

		base_url='https://graph.facebook.com/v2.10/'+user_id+'/feed/'
		url_params={}
		url_params['access_token']=access_token
		url_params['fields']='from, message, likes, created_time, place'
		r=requests.get(base_url,params=url_params)
		print (r.summary)
		posts=r.text
		posts_dict=json.loads(posts)
		for post in posts_dict['data']:
			if 'likes' not in post:
				post['likes']={}
				post['likes']['data']=[]
			post_data.append(post)

		while 'paging' in posts_dict:
			r=requests.get(posts_dict['paging']['next'])
			posts=r.text
			posts_dict=json.loads(posts)
			for post in posts_dict['data']:
				if 'likes' not in post:
					post['likes']={}
					post['likes']['data']=[]
				post_data.append(post)
		
		post_data=json.dumps(post_data)			
		cache_dict[user_id]=post_data
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_dict))
		cache_writer.close()
	return (post_data)

try:
	access_token='EAACEdEose0cBAARkqB0UO6s8Aq5om2tAOFwp9hkebe8neOu1XkbFjWzvMHoiqZA0BDhW7sISTq0sE82P4zf8vg8i45LMXWLbWkrdSjwJhonHOZBdFNTZBy76DzZAImm3bYiyMKAPG5XyGE6zQ511pb2SanyIZC0eP73Qyst3LvP0aitvhKOInLgf1ZC7dSHP8ZD'

except:
	access_token=input('\nPlease retrieve an access token from https://developers.facebook.com/tools/explorer: \n')

user_id=input('Enter user id of whoever you want to get data from.  Leave blank for yourself: \n')
if len(user_id)<1:
	user_id='me'

post_data=json.loads(get_fb_data(user_id, access_token))[:100]

print (json.dumps(post_data[0], indent=4))

conn=conn=sqlite3.connect('fb-data.sqlite')
cur=conn.cursor()

for post in post_data:
	name=post['from']['name']
	message=post['message']

cur.execute('Drop Table if Exists Posts')
cur.execute('Create Table Posts (name Varchar, message Varchar, likes Integer, time_posted Timestamp, place Varchar)')



cur.close()




