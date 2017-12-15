#This file is based on code from https://plot.ly/~colleenV/6/twitter-vs-facebook/#code
#This code creates a Bar graph to show the frequency of Facebook posts by hour

import plotly.plotly as py
from plotly.graph_objs import *
import sqlite3
import datetime
import calendar

conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

rows=cur.execute('Select time_posted from Facebook')

times={}

for row in rows:
	date_time=row[0].split('T') #Splits timestamp into date and time
	time=date_time[1] 
	hour=int(time.split(':')[0]) #Gets time from date_time and extracts the hour value, hours go from 0-23
	
	if hour not in times: #Accumulates total posts for each hour
		times[hour]=1
	else:
		times[hour]+=1

for x in range(24): #Sets value to 0 for hours not found in database
	if x not in times:
		times[x]=0
x=[]
y=[]

for hour in sorted(times.keys()): #Orders hour and frequency values in order from 0-23
	(key, value)=(hour, times[hour]) #Creates tuple with hour and number of posts as values
	x.append(key) #Splits tuple values into corresponding lists for x and y axes 
	y.append(value)

for hour in x: #Converts times from 24 hour to 12 hour
	if int(hour)==0:
		x[x.index(hour)]=str(int(hour)+12)+' am'
	
	elif int(hour)>12:
		x[x.index(hour)]=str(int(hour)-12)+' pm'

	elif int(hour)<12:
		x[x.index(hour)]=str(hour)+ ' am'
	
	elif int(hour)==12:
		x[x.index(hour)] =str(hour)+' pm'

py.sign_in('alkahan', 'vdr8fzFddzEuRqqABNzQ') 

trace1 = {
  "x": x, 
  "y": y, 
  "name": "Facebook", 
  "type": "bar"
}

data = Data([trace1])
layout = {"barmode": "group",
'title':'Facebook Posts By Hour', 
'xaxis':{'title':'Hour'},
'yaxis':{'title': 'Number of Posts'}
}
fig = Figure(data=data, layout=layout)

plot_url = py.plot(fig)

cur.close()