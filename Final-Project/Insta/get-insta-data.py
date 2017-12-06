from instagram.client import InstagramAPI


client_secret='fdf1d463d48f4d10873111cf37e8debe'
access_token='4217923875.fdf1d46.9fcca74a329148ecb6ab8c954be11ee1'

api = InstagramAPI(access_token=access_token, client_secret=client_secret)

profile=api.('self')
print (profile)

#print (api.__dir__())
# profile=api.users('self')
# print (json.dumps(profle, indent=4))
# follows=api.user_follows('self')
# print (json.dumps(follows, indent=4))
