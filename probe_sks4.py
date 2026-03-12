import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

r = requests.get('https://www.skogsstyrelsen.se/sok/?query=webbkurs', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

# Kolla alla klasser som kan vara sökresultat
for sel in ['.search-result', '.result', '.hit', '.card', '.listing', 'article']:
    els = soup.select(sel)
    if els:
        print(f'{sel}: {len(els)} element')
        print(els[0].get_text()[:200])
        print('---')

print()
# Hitta h2/h3 med länkar i main
main = soup.find('main')
if main:
    for h in main.select('h2 a, h3 a, h4 a'):
        print(h.get_text(strip=True)[:60], '|', h.get('href','')[:70])
        