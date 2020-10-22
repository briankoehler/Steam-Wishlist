import requests, json
import re
import settings
from sms import send_sales
from twilio.rest import Client


# Twilio Client
client = Client(settings.ACCOUNT_SID, settings.AUTH_TOKEN)


# API Call
response = requests.get(url='https://store.steampowered.com/wishlist/profiles/' + settings.STEAM_ID + '/wishlistdata/')
wishlist = json.loads(response.text)

# Games dictionary - names are keys, with id and plains as nested keys
games = {}
for game, info in wishlist.items():

    # id retrieval using regex on capsule url
    id = re.search('(.*)apps/(.*)/(.*)', info['capsule'])

    # plain retrieval using IsThereAnyDeal API
    plain_response = requests.get(url='https://api.isthereanydeal.com/v02/game/plain/?key=' + settings.ITAD_KEY + '&shop=steam&game_id=app%2F' + str(id.group(2)))
    plain_data = json.loads(plain_response.text)
    for key, inf in plain_data.items():
        if key == 'data':
            plain = inf['plain']

    games[info['name'].replace('amp;', '')] = {'id': id.group(2), 'plain': plain}

# Sales examiniation via ITAD API calls
sales = []
for game, info in games.items():

    # Data retrieval
    sales_response = requests.get(url='https://api.isthereanydeal.com/v01/game/prices/?region=us&key=' + settings.ITAD_KEY + '&plains=' + info['plain'])
    sales_data = json.loads(sales_response.text)

    # Price list extraction
    price_list = sales_data['data'][info['plain']]['list']

    # Examining price_cuts and comparing to PRICE_CUT
    for listing in price_list:
        if listing['price_cut'] >= settings.PRICE_CUT:
            sales.append(game + ' has a ' + str(listing['price_cut']) + '% price cut on ' + listing['shop']['name'])

# Sending all "good" sales
send_sales(sales)
