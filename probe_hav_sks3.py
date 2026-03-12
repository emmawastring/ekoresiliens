import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# HaV - kolla event-element
r = requests.get('https://www.havochvatten.se/om-oss-kontakt-och-karriar/evenemang/kalender.html', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print('=== HaV - runt 2026-03-09 ===')
idx = r.text.find('2026-03-09')
print(r.text[idx-300:idx+400])

print()

# SKS - kolla mer av sidan
r2 = requests.get('https://www.skogsstyrelsen.se/traffar-och-kurser/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
# Hitta event/kurs-element
for a in soup2.find_all('a', href=True)[:20]:
    href = a['href']
    txt = a.get_text(strip=True)
    if txt and len(txt) > 10:
        print('SKS länk:', txt[:60], '|', href[:60])