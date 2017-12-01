import requests
import json
from datetime import datetime

base_url='https://api.darksky.net/forecast/'
api_key='40ce8164d8def8fa67253db6a5bcf23b'
# api_key=dark_sky_key.api_key

lat_lng='42.280841, -83.738115'

full_url=base_url+api_key+'/'+lat_lng

response=requests.get(full_url)
data=json.loads(response.text)
hourly=data['hourly']['data']
for hour in hourly:
	print (datetime.fromtimestamp(hour['time']).day, hour['summary'], hour['temperature'])