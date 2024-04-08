import requests, os
# Spotify API Keyes
client_id = os.environ['CLIENT_ID'] 
client_secret = os.environ['CLIENT_SECERT'] 
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
}
auth_url = 'https://accounts.spotify.com/api/token'
auth_response = requests.post(auth_url, data=data,timeout=25)
access_token = auth_response.json().get('access_token')
# import re

# text = '''hello (how are you?) what worng with you (just you)'''

# # استخدم re.sub() لحذف أي فراغ كبير في بداية السطر الثاني
# print(re.sub(r'\([^)]*\)', '', text).strip('').split('\n')[0] + '\n' + re.sub(r'^\s+', '', re.sub(r'\([^)]*\)', '', text).strip('').split('\n')[1]))

