#This code is based on the py4e.com file geodump.py

import sqlite3
import codecs

conn=sqlite3.connect('206_Final.sqlite')
cur=conn.cursor()

fhand = codecs.open('geodata.js', 'w', "utf-8") #Initializing javascript cache
fhand.write("Data = [\n") #Initializes Javascript dictinary for cache

rows=cur.execute('Select message, likes, latitude, longitude, weather from Facebook') #Taking relevant data from DB

for row in rows:
	if row[-1] != None: #I only want posts with weather and location data put on the map
		message=str(row[0])
		message=message.replace("'", "") #Replaces all apostraphes in the messages because they mess up Javascript dictionary
	
		likes=str(row[1]) #I convert everything into string data
		lat=str(row[2])
		lon=str(row[3])
		weather=str(row[4])
		site='Facebook'
		
		output= "[" + lat + "," + lon + ",'" + message + "', '" + likes + "', '" + weather + "','" + site + "']" + ',\n'
		#Formats post data into JS dictionary to be added to cache file	
		fhand.write(output) #Writes dictionaries into JS cache


rows2=cur.execute('Select caption,  likes, latitude, longitude, weather from Instagram')
for row in rows2:
	if row[-1] != None:
		caption=row[0]
		caption=caption.replace("'", "")

		likes=str(row[1])
		lat=str(row[2])
		lon=str(row[3])
		weather=str(row[4])
		site='Instagram'

		output= "[" + lat + "," + lon + ",'" + caption + "','" + likes + "','" + weather+ "','" + site + "']" + ',\n'
		fhand.write(output)


fhand.write("];\n") #Ends dictionary with closing bracket and semicolon

print ('Relevant Data Has Been Saved To The JavaScript File geodata.js\n\nTo View Google Map Please Open File geodata.html\n\n')

cur.close() #Closes connection to database and JS file
fhand.close()