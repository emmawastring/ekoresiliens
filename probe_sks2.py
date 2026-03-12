import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# Events
url = 'https://www.skogsstyrelsen.se/traffar-och-kurser/?searchInput=&sort=date&counties=&skogstraff=true&digital=true&webb=true&anmalningstid=false&useFilters=true'
r = requests.get(url, headers=h, timeout=15)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print('=== SKS events ===', r.status_code)
dates = re.findall(r'202[5-9]-\d{2}-\d{2}|\d{4}-\d{2}-\d{2}', r.text)
print('Datum:', dates[:10])
idx = r.text.find('2026')
if idx > 0:
    print(r.text[idx-200:idx+400])
else:
    print(soup.get_text()[:600])

print()

# KB
r2 = requests.get('https://www.skogsstyrelsen.se/om-oss/rapporter-bocker-och-broschyrer/', headers=h, timeout=15)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print('=== SKS KB ===', r2.status_code)
dates2 = re.findall(r'202[0-9]-\d{2}-\d{2}', r2.text)
print('Datum:', dates2[:5])
# Hitta rapport-länkar
for a in soup2.find_all('a', href=True)[:20]:
    href = a['href']
    txt = a.get_text(strip=True)
    if txt and len(txt) > 15:
        print(f'  {txt[:60]} | {href[:70]}')