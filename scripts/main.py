import requests, json
import re
import configparser
from twilio.rest import Client



# Parsing settings
config = configparser.ConfigParser()
config.read('../settings.ini')
ITAD_KEY = config['keys']['itad']
STEAM_ID = config['ids']['steam']
PRICE_CUT = config.getint('misc', 'price_level')
ACCOUNT_SID = config['sms']['account_sid']
AUTH_TOKEN = config['sms']['auth_token']
PHONE_NUM = config['sms']['phone_number']

# Twilio Client
client = Client(ACCOUNT_SID, AUTH_TOKEN)


# API Call
response = requests.get(url='https://store.steampowered.com/wishlist/profiles/' + STEAM_ID + '/wishlistdata/')
wishlist = json.loads(response.text)

# Games dictionary - names are keys, with id and plains as nested keys
games = {}
for game, info in wishlist.items():

    # id retrieval using regex on capsule url
    id = re.search('(.*)apps/(.*)/(.*)', info['capsule'])

    # plain retrieval using IsThereAnyDeal API
    plain_response = requests.get(url='https://api.isthereanydeal.com/v02/game/plain/?key=' + ITAD_KEY + '&shop=steam&game_id=app%2F' + str(id.group(2)))
    plain_data = json.loads(plain_response.text)
    for key, inf in plain_data.items():
        if key == 'data':
            plain = inf['plain']

    games[info['name'].replace('amp;', '')] = {'id': id.group(2), 'plain': plain}

# Sales examiniation via ITAD API calls
for game, info in games.items():

    # Data retrieval
    sales_response = requests.get(url='https://api.isthereanydeal.com/v01/game/prices/?region=us&key=' + ITAD_KEY + '&plains=' + info['plain'])
    sales_data = json.loads(sales_response.text)

    # Price list extraction
    price_list = sales_data['data'][info['plain']]['list']

    # Examining price_cuts and comparing to PRICE_CUT |||| message = client.messages.create(to=PHONE_NUM, from_='+15593376358', body='Test message')
    for listing in price_list:
        if listing['price_cut'] > PRICE_CUT:
            print(game + ' has a ' + str(listing['price_cut']) + '% price cut on ' + listing['shop']['name'])
