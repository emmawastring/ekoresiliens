import requests, re
h = {'User-Agent': 'Mozilla/5.0'}
r = requests.get('https://www.naturvardsverket.se/soksida/?q=evenemang&p=1', headers=h)
print('Status:', r.status_code)

# Hitta JSON i script-taggar
from bs4 import BeautifulSoup
soup = BeautifulSoup(r.text, 'html.parser')
for s in soup.find_all('script'):
    t = s.string or ''
    if 'heading' in t and 'url' in t:
        print('Script med heading+url:')
        print(t[:600])
        break

# Kolla runt 'heading' i rå HTML
idx = r.text.find('"heading"')
if idx > 0:
    print('\nRå HTML runt heading:')
    print(r.text[idx-100:idx+300])