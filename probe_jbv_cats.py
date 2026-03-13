import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0', 'Accept-Charset': 'utf-8'}

BASE = 'https://webbutiken.jordbruksverket.se'
r = requests.get(f'{BASE}/sv/artiklar/rapporter/index.html', headers=h, timeout=15)
r.encoding = 'iso-8859-1'
soup = BeautifulSoup(r.text, 'html.parser')

print('Alla kategorier:')
for a in soup.find_all('a', href=True):
    href = a['href']
    txt = a.get_text(strip=True)
    if '/sv/artiklar/' in href and txt and len(txt) > 3:
        print(f'  {txt[:60]} | {href}')