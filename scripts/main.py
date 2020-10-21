import requests, json
import re
import configparser



# Parsing settings
config = configparser.ConfigParser()
config.read('../settings.ini')
itad_key = config['keys']['itad']
steam_id = config['ids']['steam']



# API Call
response = requests.get(url='https://store.steampowered.com/wishlist/profiles/' + steam_id + '/wishlistdata/')
wishlist = json.loads(response.text)

# Games dictionary - names are keys, with id and plains as nested keys
games = {}
for game, info in wishlist.items():

    # id retrieval using regex on capsule url
    id = re.search('(.*)apps/(.*)/(.*)', info["capsule"])

    # plain retrieval using IsThereAnyDeal API
    plain_response = requests.get(url='https://api.isthereanydeal.com/v02/game/plain/?key=' + itad_key + '&shop=steam&game_id=app%2F' + str(id.group(2)))
    plain_data = json.loads(plain_response.text)
    plain = None
    for key, inf in plain_data.items():
        if key == "data":
            plain = inf["plain"]

    games[info["name"].replace("amp;", "")] = {"id": id.group(2), "plain": plain}
