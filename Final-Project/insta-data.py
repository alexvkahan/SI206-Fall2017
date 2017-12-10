import requests
import json
import insta_token
import sqlite3

base_url='https://api.instagram.com/v1/users/'

access_token=insta_token.access_token #takes my access token from insta_token.py

cache_fname='insta-data.json'

try:
	cache_file=open(cache_fname, 'r')
	cache_contents=cache_file.read()
	cache_diction=json.loads(cache_contents)

except:
	cache_diction={}

def get_data(user_id):
	
	if user_id in cache_diction:
		print ('Using cached data')
		post_data=cache_diction[user_id]
	
	else:
		print ('Fetching data from Instagram')
		r=requests.get(base_url+user_id+'/media/recent?access_token='+access_token)
		post_data=r.text
		cache_diction[user_id]=post_data
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_diction))
		cache_writer.close()
	
	return (post_data)

user_id=input('Enter the user id of whoever you want to get post data from.  Leave blank for yourself: ')
if len(user_id)<1:
	user_id='self'

insta_posts=json.loads(get_data(user_id))

conn=conn=sqlite3.connect('insta-data.sqlite')
cur=conn.cursor()

cur.execute('DROP TABLE if EXISTS Posts')
cur.execute('''Create Table Posts (name Varchar, caption Varchar, likes Integer, time_posted Timestamp, latitude Varchar, longitude Varcahar)''')

post_data=insta_posts['data']

print (json.dumps(post_data[0], indent=4))

for post in post_data:
	name=post['user']['full_name']
	caption=post['caption']['text']
	likes=post['likes']['count'] 
	time=post['created_time']
	
	try:
		latitude=post['location']['latitude']
		longitude=post['location']['longitude']
	
	except:
		latitude=''
		longitude=''
	
	tup=(name, caption, likes, time, latitude, longitude)
	
	cur.execute('Insert into Posts (name, caption, likes, time_posted, latitude, longitude) values (?,?,?,?,?,?)', tup)

conn.commit()
cur.close()










