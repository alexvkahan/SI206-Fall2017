from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

url='http://py4e-data.dr-chuck.net/comments_38734.html'

html=urlopen(url, context=ctx).read()

soup=BeautifulSoup(html, 'html.parser')
x=soup.find_all('span')

total=0
for item in x:
	y=item.contents
	for number in y:
		number=int(number)
		total+=number
print (total)

