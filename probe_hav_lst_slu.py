import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# HaV - kolla fler event-element och paginering
r = requests.get('https://www.havochvatten.se/om-oss-kontakt-och-karriar/evenemang/kalender.html', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
items = soup.select('a.hav-list__items--item-link')
print(f'HaV event-länkar: {len(items)}')
for a in items[:5]:
    href = a.get('href','')
    title = a.get('title','') or a.get_text(strip=True)
    m = re.search(r'/(\d{4}-\d{2}-\d{2})-', href)
    date = m.group(1) if m else '?'
    print(f'  {date} | {title[:60]}')

print()

# Länsstyrelsen Skåne - ny URL
r2 = requests.get('https://www.lansstyrelsen.se/skane/om-oss/kalender/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print('Lst Skåne status:', r2.status_code)
dates = re.findall(r'20\d{2}-\d{2}-\d{2}', r2.text)
print('Datum:', dates[:5])
idx = r2.text.find('202')
print(r2.text[idx-100:idx+300])

print()

# SLU sok struktur
r3 = requests.get('https://www.slu.se/sok/?q=evenemang&type=calendar', headers=h, timeout=10)
r3.encoding = 'utf-8'
print('SLU sok calendar:', r3.status_code)
dates3 = re.findall(r'20\d{2}-\d{2}-\d{2}', r3.text)
print('Datum:', dates3[:5])