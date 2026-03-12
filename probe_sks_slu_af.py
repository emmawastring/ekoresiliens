import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# Skogsstyrelsen - sök
for url in [
    'https://www.skogsstyrelsen.se/sok/?q=webbinarium',
    'https://www.skogsstyrelsen.se/sok/?q=kurs',
    'https://www.skogsstyrelsen.se/traffar-och-kurser/digitala-traffar/',
]:
    try:
        r = requests.get(url, headers=h, timeout=8)
        dates = re.findall(r'202[5-9]-\d{2}-\d{2}', r.text)
        print(f'{r.status_code} {url.split("/")[-2] or url.split("/")[-1]}: datum={dates[:3]}')
    except Exception as e:
        print(f'ERR: {e}')

print()

# SLU nyheter - kolla search-hit struktur mer
r2 = requests.get('https://www.slu.se/kalender/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
hits = soup2.select('.search-hit')
print(f'SLU hits: {len(hits)}')
for hit in hits[:3]:
    date = hit.select_one('.search-hit__metainfo')
    title = hit.select_one('.search-hit__title a')
    print(f'  {date.get_text(strip=True) if date else "?"} | {title.get_text(strip=True)[:60] if title else "?"}')
    print(f'  url: {title.get("href","")[:80] if title else "?"}')

print()

# agroforestry.se KB-sidor
r3 = requests.get('https://agroforestry.se/', headers=h, timeout=10)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
print('agroforestry.se sidor:')
for a in soup3.find_all('a', href=True):
    href = a['href']
    if 'agroforestry.se/' in href and href.count('/') >= 4:
        txt = a.get_text(strip=True)
        if txt and len(txt) > 3:
            print(f'  {txt[:50]} | {href[:70]}')