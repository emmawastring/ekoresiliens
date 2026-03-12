import requests
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# Skogsstyrelsen - kolla startsida för kalender-länk
r = requests.get('https://www.skogsstyrelsen.se/', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all('a', href=True):
    href = a['href']
    if any(x in href for x in ['kalen', 'event', 'kurs', 'utbildn', 'aktuellt']):
        print('SKS:', href[:80])

print()

# HaV - kolla startsida
r2 = requests.get('https://www.havochvatten.se/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
for a in soup2.find_all('a', href=True):
    href = a['href']
    if any(x in href for x in ['kalen', 'event', 'kurs', 'aktuellt', 'nyheter']):
        print('HaV:', href[:80])

print()

# SLU sok - kolla strukturen
r3 = requests.get('https://www.slu.se/sok/?q=evenemang', headers=h, timeout=10)
r3.encoding = 'utf-8'
import re
dates = re.findall(r'20\d{2}-\d{2}-\d{2}', r3.text)
print('SLU datum:', dates[:5])
idx = r3.text.find('evenemang')
print('SLU html-snippet:', r3.text[idx:idx+300])