import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# På gång - hitta event-text mer exakt
r = requests.get('https://www.underekarna.se/p%C3%A5-g%C3%A5ng/', headers=h)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print('=== PÅ GÅNG - HTML runt events ===')
idx = r.text.find('Webbinarium')
print(r.text[idx-200:idx+600])

print()

# Förädling - kolla article titel och länk
r3 = requests.get('https://www.underekarna.se/f%C3%B6r%C3%A4dling/', headers=h)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
print('=== FÖRÄDLING - titlar och länkar ===')
for art in soup3.select('article')[:5]:
    a = art.find('a', href=True)
    h2 = art.find('h2') or art.find('h3') or art.find('h4')
    p = art.find('p')
    print('  titel:', h2.get_text(strip=True)[:60] if h2 else '-')
    print('  länk:', a.get('href','')[:60] if a else '-')
    print('  text:', p.get_text(strip=True)[:80] if p else '-')
    print()