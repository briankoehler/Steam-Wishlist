import requests, json
import settings
from bs4 import BeautifulSoup


HEADERS = {
    'Accept-Language': 'en-US;q=0.7,en;q=0.3',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}


# API Call
response = requests.get(url='https://store.steampowered.com/wishlist/profiles/' + settings.STEAM_ID + '/wishlistdata/')
wishlist = json.loads(response.text)

# Games list
games = []
sales = {}
for game, info in wishlist.items():
    games.append(info['name'].replace('amp;', ''))

# Searching G2A
for game in games:

    # Retrieving HTML
    response = requests.get(url='https://www.g2a.com/search?query=' + game, headers=HEADERS)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Analyzing results
    results = soup.find_all('div', class_='Card__base')
    x = 0
    for result in results:
        title = result.find('h3', class_='Card__title').find('a').text
        if game not in title:
            break;
        if 'GLOBAL' in title or 'NORTH AMERICA' in title:
            try:
                price_cut = (result.find('span', class_='discount-info--percent discount-info--percent__bg-red').text)[1:-1]
                if int(price_cut) >= settings.PRICE_CUT:
                    sales[title] = price_cut
            except AttributeError:
                continue
        x += 1
        if x == 4:
            break

print(sales)