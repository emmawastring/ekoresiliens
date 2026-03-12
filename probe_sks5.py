import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

url = 'https://www.skogsstyrelsen.se/traffar-och-kurser/?searchInput=&sort=date&counties=&skogstraff=true&digital=true&webb=true&anmalningstid=true&useFilters=true'
r = requests.get(url, headers=h, timeout=15)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

print('Status:', r.status_code)
dates = re.findall(r'202[5-9]-\d{2}-\d{2}', r.text)
print('Datum:', dates[:10])

# Kolla om data finns i script/json
for s in soup.find_all('script'):
    t = s.string or ''
    if any(x in t for x in ['datum', 'date', 'title', 'kurs', 'traff']):
        print('Script med data:', t[:400])
        print('---')

# Kolla main-innehåll
main = soup.find('main')
if main:
    print(main.get_text()[:600])