import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# 1. Epsilon – kolla tabellinnehåll
print('=== EPSILON TABELLER ===')
url = 'https://stud.epsilon.slu.se/cgi/search/archive/advanced?dataset=archive&screen=Search&documents_merge=ALL&documents=&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&abstract_merge=ALL&abstract=&date=&series_merge=ALL&series=&keywords_merge=ANY&keywords=Milj%C3%B6%2C+klimat+%2C+klimatanpassning%2C+resiliens%2C+stadsplanering%2C+perenn%2C+naturbaserade+l%C3%B6sningar%2C+dagvatten%2C+skyfall%2C+ekosystemtj%C3%A4nster%2C+h%C3%A5llbarhet%2C+cirkul%C3%A4ritet&language=eng&language=swe&satisfyall=ALL&order=yearofpub%2Fcreators_name%2Ftitle&_action_search=S%C3%B6k'
r = requests.get(url, headers=h, timeout=20)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

# Skriv ut alla tabeller
for i, t in enumerate(soup.find_all('table')):
    txt = t.get_text(strip=True)
    if len(txt) > 50:
        print(f'Tabell {i}: {txt[:300]}')
        print('---')
        # Kolla länkar i tabellen
        for a in t.find_all('a', href=True)[:5]:
            print(f'  LÄNK: {a.get_text(strip=True)[:60]} | {a["href"][:80]}')

# 2. LBN – kolla event-sidan mer ingående
print('\n=== LBN EVENTS DJUP ===')
r2 = requests.get('https://www.landsbygdsnatverket.se/kommandeaktiviteter.4.490b482015189b53667216b.html', headers=h, timeout=15)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')

# Kolla h2 med sina föräldrar för att hitta datum och länkar
for h2 in soup2.find_all('h2')[:5]:
    parent = h2.find_parent(['article', 'div', 'section', 'li'])
    if parent:
        txt = parent.get_text(' ', strip=True)
        links = parent.find_all('a', href=True)
        print(f'H2: {h2.get_text(strip=True)[:70]}')
        print(f'  Text: {txt[:150]}')
        for a in links[:2]:
            print(f'  Länk: {a["href"][:80]}')