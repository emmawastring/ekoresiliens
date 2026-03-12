import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# SLU - kolla soksidan mer
for url in [
    'https://www.slu.se/sok/?q=evenemang&facet=calendar',
    'https://www.slu.se/sok/?q=kurs+webbinarium',
    'https://www.slu.se/kalender/',
    'https://www.slu.se/om-slu/kalender-och-evenemang/',
]:
    r = requests.get(url, headers=h, timeout=8)
    dates = re.findall(r'202[5-9]-\d{2}-\d{2}', r.text)
    print(f'{r.status_code} {url.split("/")[-2]}: datum={dates[:3]}')

print()

# SKS - kolla traffar-och-kurser djupare
r2 = requests.get('https://www.skogsstyrelsen.se/traffar-och-kurser/', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
dates2 = re.findall(r'202[5-9]-\d{2}-\d{2}|\d{4}-\d{2}-\d{2}', r2.text)
print('SKS datum:', dates2[:5])
idx = r2.text.find('kurs')
print(r2.text[idx:idx+400])