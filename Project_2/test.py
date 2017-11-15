import unittest
import requests
import re
from bs4 import BeautifulSoup
import ssl
from urllib.request import urlopen


## PART 3 (a) Define a function called get_umsi_data.  It should create a dictionary
## saved in a variable umsi_titles whose keys are UMSI people's names, and whose 
## associated values are those people's titles, e.g. "PhD student" or "Associate 
## Professor of Information"...
## Start with this page: https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All  
## End with this page: https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All&page=12 
## INPUT: N/A. No input.
## OUTPUT: Return umsi_titles
## Reminder: you'll need to use the special header for a request to the UMSI site, like so:
## requests.get(base_url, headers={'User-Agent': 'SI_CLASS'}) 

def get_umsi_data():
    umsi_titles={}
    base_url='https://www.si.umich.edu/directory?field_person_firstname_value=&field_person_lastname_value=&rid=All'

    
    while True: 
        result=requests.get(base_url, headers={'User-Agent': 'SI_CLASS'})
        soup=BeautifulSoup(result.content, 'html.parser')
        directory=soup(class_='view-content')
        for people in directory:
            people=people(class_='views-row')
            for person in people:
                name=(person('h2'))[-1]
                name=name.text
                title=person(class_='field-item even')
                title=(title[-1].text)
                umsi_titles[name]=title
                
       
        pager=soup(class_='pager-next')
        for page in pager:
            href=page('a')
            for link in href:
                link=link.get('href', None)
                print (link)
                if len(link)>0:
                    base_url='https://www.si.umich.edu'+link
                else:
                	return (umsi_titles)

                
    
		

data=get_umsi_data()
print (len(data))
# def num_students(data):
# 	phd=0
# 	for person in data.keys():
# 		if data[person]=='PhD student':
# 			phd+=1
# 	return (phd)


# num_students(data)
    		
    	
    



    




