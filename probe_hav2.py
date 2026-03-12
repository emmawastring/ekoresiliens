import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# HaV - kolla title-formatet mer
r = requests.get('https://www.havochvatten.se/om-oss-kontakt-och-karriar/evenemang/kalender.html', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
items = soup.select('a.hav-list__items--item-link')
print('HaV titles:')
for a in items[:8]:
    print(' ', a.get('title','')[:80])

print()

# Lst Skane - kolla event-element
r2 = requests.get('https://www.lansstyrelsen.se/skane/om-oss/kalender/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
# Kolla alla länkar med datum
for a in soup2.find_all('a', href=True):
    href = a['href']
    if 'kalender' in href and '202' in href:
        print('Lst:', a.get_text(strip=True)[:60], '|', href[:80])
print()
# Kolla text
print(soup2.get_text()[:800])