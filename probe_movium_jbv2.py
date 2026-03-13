import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# 1. Movium Fakta – hämta alla PDF-länkar
print('=== MOVIUM FAKTA ===')
r = requests.get('https://movium.slu.se/soek/?q=movium+fakta', headers=h, timeout=15)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all('a', href=True):
    href = a['href']
    txt = a.get_text(strip=True)
    if 'fakta' in (href+txt).lower() or '.pdf' in href.lower():
        print(f'  {txt[:70]} | {href[:80]}')

# 2. Movium Nyheter – kolla article/div-struktur
print('\n=== MOVIUM NYHETER ===')
r2 = requests.get('https://movium.slu.se/nyheter/', headers=h, timeout=15)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
# Hitta nyhetslänkar
for a in soup2.find_all('a', href=True):
    href = a['href']
    if '/nyheter/' in href and href != '/nyheter/':
        print(f'  {a.get_text(strip=True)[:70]} | {href[:80]}')
print(f'Totalt nyhetslänkar: {len([a for a in soup2.find_all("a", href=True) if "/nyheter/" in a["href"] and a["href"] != "/nyheter/"])}')

# 3. JBV Webbutik – kategorier
print('\n=== JBV WEBBUTIK kategorier ===')
r3 = requests.get('https://webbutiken.jordbruksverket.se/', headers=h, timeout=15)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
for a in soup3.find_all('a', href=True):
    href = a['href']
    txt = a.get_text(strip=True)
    if txt and len(txt) > 3 and 'jordbruksverket' in href and not any(x in href for x in ['bestall', 'kassan', 'cgi-bin', 'en/']):
        print(f'  {txt[:60]} | {href[:80]}')