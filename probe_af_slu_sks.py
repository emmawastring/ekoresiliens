import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# agroforestry.se
r = requests.get('https://agroforestry.se/', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print('=== agroforestry.se ===')
for a in soup.find_all('a', href=True):
    href = a['href']
    if any(x in href for x in ['event', 'kalen', 'kurs', 'aktivitet']):
        print(' ', href[:80])

print()

# SLU /kalender/
r2 = requests.get('https://www.slu.se/kalender/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print('=== SLU /kalender/ ===', r2.status_code)
idx = r2.text.find('2026-03-12')
print(r2.text[idx-200:idx+400])

print()

# SKS - kolla om det finns event-data djupare
r3 = requests.get('https://www.skogsstyrelsen.se/traffar-och-kurser/', headers=h, timeout=10)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
# Hitta event-liknande element
for a in soup3.find_all('a', href=True):
    href = a['href']
    txt = a.get_text(strip=True)
    if 'traff' in href or 'kurs' in href and '202' in href:
        print('SKS:', txt[:50], '|', href[:70])