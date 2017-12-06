import requests
import facebook
import json
import fb_info

try:
	access_token='EAACEdEose0cBAJwj6QppZBtJkX9n7rvrsf8C6E9t9ZCNEZCELRfZCqNua4USmxwqfQnQUJitgT0MvX0ZAZCRkL1ZB6BZCZCZBcxoPMNJHZAOFiJT9SKZCQuLPQC6vrmCHnIiF0m6ARskHBxjaGArBHw6esyzNbThZAZA8W09SEhGrTjf3ZBznSZA0fKEjFsn1qXoFZAvn6SYZD'
except:
	access_token=input('\nPlease retrieve an access token from https://developers.facebook.com/tools/explorer\n')

graph = facebook.GraphAPI(access_token)
friends=graph.get_connections('me', 'friends')

print (json.dumps(friends, indent=4))


