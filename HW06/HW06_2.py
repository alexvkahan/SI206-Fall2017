import urllib.request, urllib.parse, urllib.error
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
y='http://py4e-data.dr-chuck.net/known_by_Kenzeigh.html'
url =  input('Enter URL: ')

count=int(input('Enter Count: '))
position=int(input('Enter Position: '))

x=0
while x<count:
	html = urllib.request.urlopen(url, context=ctx).read()
	soup = BeautifulSoup(html, 'html.parser')
	tags = soup('a')
	tag=tags[position]
	link=tag.get('href', None)
	print ('Retrieving: ', link)
	url=link
	x+=1
