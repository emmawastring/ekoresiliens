import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

for url in [
    'https://www.skogsstyrelsen.se/sok/?query=webbkurs',
    'https://www.skogsstyrelsen.se/sok/?query=webbinarium',
    'https://www.skogsstyrelsen.se/sok/?query=kurs',
]:
    r = requests.get(url, headers=h, timeout=10)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    dates = re.findall(r'202[5-9]-\d{2}-\d{2}', r.text)
    print(f'=== {url.split("=")[-1]} ({r.status_code}) ===')
    print('Datum:', dates[:5])
    idx = r.text.find('202')
    if idx > 0:
        print(r.text[idx-100:idx+400])
    print()