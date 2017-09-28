import re
mbox=open('mbox-short.txt')

for line in mbox:
	if re.search('From',line):
		print (line)
		numbers=re.findall('[0-9]+',line)
		print (numbers)
		name=re.findall('(\S*)@',line)
		print (name)


	