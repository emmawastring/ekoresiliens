import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# SLU - kolla search-hit struktur
r = requests.get('https://www.slu.se/kalender/', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
hits = soup.select('.search-hit')
print(f'SLU search-hits: {len(hits)}')
if hits:
    print(hits[0].prettify()[:600])

print()

# SLU - finns det filtrering för bara evenemang?
for url in [
    'https://www.slu.se/kalender/?type=event',
    'https://www.slu.se/kalender/?filter=event',
    'https://www.slu.se/kalender/?q=webbinarium',
]:
    r2 = requests.get(url, headers=h, timeout=8)
    hits2 = BeautifulSoup(r2.text, 'html.parser').select('.search-hit')
    print(f'{r2.status_code} {url.split("?")[-1]}: {len(hits2)} hits')

print()

# agroforestry.se - kolla alla sidor
r3 = requests.get('https://agroforestry.se/', headers=h, timeout=10)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
print('agroforestry.se menylänkar:')
for a in soup3.select('nav a, .menu a, header a'):
    print(' ', a.get_text(strip=True)[:40], '|', a.get('href','')[:60])