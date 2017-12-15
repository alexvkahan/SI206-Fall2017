#This file is based on code from https://plot.ly/~colleenV/6/twitter-vs-facebook/#code
#This file creates a side by side bar graph to show the average likes for Facebook and Instagram posts posted on each day

import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
import datetime
import calendar

conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

rows=cur.execute('Select likes, time_posted from Facebook') 

days={}

for row in rows:
	likes=row[0]

	date_time=row[1].split('T') #Splits timestamp into date and time
	date=datetime.datetime.strptime(date_time[0], '%Y-%M-%d') #Creates datetime obkect by stripping date
	day=datetime.datetime.weekday(date) ##Gets numerical value for day of the week Monday is 0, Sunday is 6
	
	if day not in days: #Creates dictionaries of like counts for each day into dictionary days
		days[day]=[likes]
	else:
		days[day].append(likes)

x=[]
y=[]

for day in sorted(days.keys()): #Orders days of the week Monday-Sunday
	(key, value)=(calendar.day_name[day], sum(days[day])/len(days[day])) #Converts numerical day value into word, divides total likes by number of posts for each individual day
	#Creates tuple with day of the week and average likes as values, then separates them into lists for the x and y axes
	x.append(key)
	y.append(value)

days2={} #Repeats process for Instagram posts

rows2=cur.execute('Select likes, time_posted from Instagram')
for row in rows:	
	likes=row[0]

	date_time=row[1] #Creates datetime object from Unix timestamp
	date=datetime.datetime.fromtimestamp(date_time)
	day=datetime.datetime.weekday(date)	

	if day not in days2:
		days2[day]=[likes]
	else:
		days2[day].append(likes)

w=[]
z=[]

for day in sorted(days2.keys()):
	(key, value)= (calendar.day_name[day], sum(days2[day])/len(days2[day]))
	
	w.append(key)
	z.append(value)

py.sign_in('alkahan', 'vdr8fzFddzEuRqqABNzQ')
trace1 = {
  "x": x, #Appropriate values for days of the weeks and average likes loaded into trace object for Instagram and Facebook
  "y": y, 
  "name": "Facebook", 
  "type": "bar"
}

trace2 = {
  "x": w, 
  "y": z, 
  "name": "Instagram", 
  "type": "bar"
}

data = Data([trace1, trace2])
layout = {"barmode": "group",
'title':'Facebook VS Instagram Average Likes By Day',
'xaxis':{'title':'Day of the Week'},
'yaxis':{'title': 'Average Likes'}
}
fig = Figure(data=data, layout=layout)

plot_url = py.plot(fig)

cur.close()