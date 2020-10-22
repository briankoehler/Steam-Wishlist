import requests
from bs4 import BeautifulSoup

url = 'https://www.g2a.com/search?query=doom eternal'

headers = {
    'Accept-Language': 'en-US;q=0.7,en;q=0.3',
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.content, 'html.parser')


results = soup.find_all('div', class_='Card__base')

titles = []
games = {}
x = 0
for result in results:
    card_title = result.find('h3', class_='Card__title')
    title = card_title.find('a').text
    if 'GLOBAL' in title or 'NORTH AMERICA' in title:
        price_cut = result.find('span', class_='discount-info--percent discount-info--percent__bg-red').text
        games[title] = price_cut
    x += 1
    if x == 4:
        break
    
print(games)