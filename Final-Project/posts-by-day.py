#This file is based on code from https://plot.ly/~colleenV/6/twitter-vs-facebook/#code
#This code creates a side by side bar graph to show the number of posts per day for Instagram and Facebook

import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
import datetime
import calendar

conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

rows=cur.execute('Select time_posted from Facebook')

days={}

for row in rows:
	date_time=row[0].split('T') #splits timestamp into dat and time
	date=datetime.datetime.strptime(date_time[0], '%Y-%M-%d') #Creates datetime object by stripping date
	day=datetime.datetime.weekday(date) #From datetime object creates numerical values for day of the week, Monday is 0, Sunday is 6
	
	if day not in days: #Accumulates total posts for each day
		days[day]=1
	else:
		days[day]+=1

x=[]
y=[]
for day in sorted(days.keys()): #Orders days of the week Monday-Sunday
	(key,value)=(calendar.day_name[day], days[day]) #Converts numerical day value to word
	#Creates tuple with day of the week and number of posts as values
	x.append(key) #Splits tuple into corresponding lists for x and y axes
	y.append(value)

rows2=cur.execute('Select time_posted from Instagram') #Repeats for Instagram posts

days2={}

for row in rows2: #Repeats for Instagram data
	date_time=row[0] 
	date=datetime.datetime.fromtimestamp(date_time) #Converts Unix timestamp to datetime object
	day=datetime.datetime.weekday(date)	

	if day not in days2:
		days2[day]=1
	else:
		days2[day]+=1
w=[]
z=[]
for day in sorted(days2.keys()):
	(key,value)=(day, days2[day])
	w.append(calendar.day_name[day])
	z.append(value)


py.sign_in('alkahan', 'vdr8fzFddzEuRqqABNzQ')
trace1 = {
  "x": x, 
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
'title':'Facebook VS Instagram Posts By Day', 
'xaxis':{'title':'Day of the Week'},
'yaxis':{'title':'Number of Posts'}
}
fig = Figure(data=data, layout=layout)

plot_url = py.plot(fig)
cur.close()
