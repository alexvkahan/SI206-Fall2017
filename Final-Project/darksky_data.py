import requests
import sqlite3
import json
import darksky_key

cache_fname='darsky_data.json'
secret_key=darksky_key.secret_key
base_url='https://api.darksky.net/forecast/'+secret_key+'/'

try:
	cache_file=open(cache_fname, 'r')
	cache_contents=cache_file.read()
	cache_diction=json.loads(cache_contents)

except:
	cache_diction={}

def get_fb_weather_data():
	if 'facebook' in cache_diction:
		print ('Using Cached Data\n\n')
		weather_data=cache_diction['facebook']
	
	else:
		print ('Fetching weather data from Darksky\n\n')
		conn=sqlite3.connect('206_final.sqlite')
		cur=conn.cursor()
		rows=cur.execute('Select id, time_posted, longitude, latitude from Facebook')
		weather_data=[]
		for row in rows:	
			if len(str(row[2]))>0:
				row_lst=[]
			
				for item in row:
					row_lst.append(item)
				row_lst[1]=row_lst[1][:-5]

				r=requests.get(base_url+row_lst[3]+','+row_lst[2]+','+row_lst[1])
				weather_data.append(json.loads(r.text))
		cur.close()
		cache_diction['facebook']=weather_data
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_diction))
		cache_writer.close()

	return (weather_data)

def get_insta_weather_data():
	if 'instagram' in cache_diction:
		print ('Using Cached Data')
		weather_data=cache_diction['instagram']

	else:
		print ('Fetching weather data from Darksky')
		conn=sqlite3.connect('206_final.sqlite')
		cur=conn.cursor()
		rows=cur.execute('Select id, time_posted, longitude, latitude from Instagram')
		weather_data=[]
		for row in rows:
			if len(str(row[2]))>0:
				row_lst=[]
			
				for item in row:
					row_lst.append(item)

				r=requests.get(base_url+str(row_lst[3])+','+str(row_lst[2])+','+str(row_lst[1]))
				weather_data.append(json.loads(r.text))
		cur.close()
		cache_diction['instagram']=weather_data
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_diction))
		cache_writer.close()

	return (weather_data)

fb_weather=get_fb_weather_data()

conn=conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

for weather in fb_weather:
	latitude=weather['latitude']
	longitude=weather['longitude']
	weather_summary=weather['currently']['summary']
	temp=str(weather['currently']['temperature'])




	





