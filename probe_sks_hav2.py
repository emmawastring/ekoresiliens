import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# SKS träffar och kurser
r = requests.get('https://www.skogsstyrelsen.se/traffar-och-kurser/', headers=h, timeout=10)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print('=== SKS /traffar-och-kurser/ ===', r.status_code)
dates = re.findall(r'20\d{2}-\d{2}-\d{2}|\d{1,2}\s+\w+\s+20\d{2}', r.text)
print('Datum:', dates[:5])
print(soup.get_text()[:600])

print()

# HaV kalender
r2 = requests.get('https://www.havochvatten.se/om-oss-kontakt-och-karriar/evenemang/kalender.html', headers=h, timeout=10)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print('=== HaV kalender ===', r2.status_code)
dates2 = re.findall(r'20\d{2}-\d{2}-\d{2}', r2.text)
print('Datum:', dates2[:5])
print(soup2.get_text()[:600])

print()

# HaV extern kalender 2026
r3 = requests.get('https://www.havochvatten.se/om-oss-kontakt-och-karriar/evenemang/kalender/kalender/2026/extern-kalender-2026.html', headers=h, timeout=10)
r3.encoding = 'utf-8'
print('=== HaV extern 2026 ===', r3.status_code)
print(r3.text[:400])