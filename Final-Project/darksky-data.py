#This code takes time and geodata for Facebook and Instagram posts to find historical weather data from the Darksky API

import requests
import sqlite3
import json
import darksky_key

cache_fname='darksky-data.json' #Raw weather data is saved to cache file
key=darksky_key.secret_key #imports my darksky api secret key
base_url='https://api.darksky.net/forecast/'+key+'/'

try:
	cache_file=open(cache_fname, 'r')
	cache_contents=cache_file.read()
	cache_diction=json.loads(cache_contents)

except:
	cache_diction={}

def get_fb_weather_data(): #This function gets Facebook data from database and requests weather data from Darksky
	
	if 'facebook' in cache_diction: #If facebook data is in cache, uses cached data
		print ('Using Cached Facebook Weather Data\n\n')
		weather_data=cache_diction['facebook']
	
	else: #If data is not in cache file, requests data from Darksky
		print ('Fetching Facebook Weather Data From Darksky\n\n')
		conn=sqlite3.connect('206_final.sqlite')
		cur=conn.cursor()
		rows=cur.execute('Select time_posted, longitude, latitude from Facebook')
		weather_data=[]
		
		for row in rows:	
			time=str(row[0]) #Converts each data point into string
			latitude=str(row[2])
			longitude=str(row[1])
			
			if len(latitude)>0: #Only requests weather data if geodata is available
				r=requests.get(base_url+latitude+','+longitude+','+time)
				weather_data.append(json.loads(r.text))
		
		cur.close()
		cache_diction['facebook']=weather_data #Writes weather data to cache file
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_diction))
		cache_writer.close()

		print ('Weather Data For Facebook Posts Has Been Saved To The Cache File darksky-data.py\n\n')

	return (weather_data)

def get_insta_weather_data(): #Repeats process for Instagram Data
	if 'instagram' in cache_diction:
		print ('Using Cached Instagram Weather Data\n\n')
		weather_data=cache_diction['instagram']

	else:
		print ('Fetching Instagram Weather Data From Darksky\n\n')
		conn=sqlite3.connect('206_final.sqlite')
		cur=conn.cursor()
		rows=cur.execute('Select time_posted, longitude, latitude from Instagram')
		weather_data=[]
		
		for row in rows:
			time=str(row[0])
			latitude=str(row[2])
			longitude=str(row[1])
			
			if len(latitude)>0:
				r=requests.get(base_url+latitude+','+longitude+','+time)
				weather_data.append(json.loads(r.text))
		cur.close()
		cache_diction['instagram']=weather_data
		cache_writer=open(cache_fname, 'w')
		cache_writer.write(json.dumps(cache_diction))
		cache_writer.close()

		print ('Weather Data For Instagram Posts Has Been Saved To The Cache File darksky-data.py\n\n')

	return (weather_data)

fb_weather=get_fb_weather_data() #Calls functions to request Facebook weather data
insta_weather=get_insta_weather_data() #Calls function to request Instagram weather data

conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

for weather in fb_weather: #Extracts data points from weather data
	latitude=str(weather['latitude'])
	longitude=str(weather['longitude'])
	summary=str(weather['currently']['summary']) 
	temp=str(weather['currently']['temperature'])
	weather_summary=temp+' '+summary

	cur.execute('Update Facebook Set Weather=(?) where latitude=(?)', (weather_summary, latitude)) #Updates database to include weather data for relevant Facebook posts
	conn.commit()

for weather in insta_weather:
	latitude=str(weather['latitude'])
	longitude=weather['longitude']
	summary=weather['currently']['summary']
	temp=str(weather['currently']['temperature'])
	weather_summary=temp+' '+summary

	cur.execute('Update Instagram Set Weather=(?) where latitude=(?)', (weather_summary, latitude)) #Updates database to include weather data for relevant Instagram posts
	conn.commit()

cur.close()

print ('The Database 206_final.sqlite Has Been Updated With Weather Data For Facebook and Instagram Posts That Include Geodata\n\n')



	





