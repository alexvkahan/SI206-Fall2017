import instagram
print (instagram)


client_id='fdf1d463d48f4d10873111cf37e8debe'
access_token='4217923875.fdf1d46.9fcca74a329148ecb6ab8c954be11ee1'

api = InstagramAPI(access_token=access_token, client_secret=client_secret)

follows=api.user_follows('me')
print (json.dumps(follows, indent=4))
