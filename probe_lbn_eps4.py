import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

BASE_LBN = 'https://www.landsbygdsnatverket.se'

# 1. LBN – kolla en event-detaljsida
print('=== LBN EVENT-DETALJ ===')
url = BASE_LBN + '/kommandeaktiviteter/kalenderaktiviteter/webbinariumomstodochersattningarframove'
try:
    r = requests.get(url, headers=h, timeout=15)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    print(f'Status: {r.status_code}')
    dates_iso = re.findall(r'202[0-9]-\d{2}-\d{2}', r.text)
    dates_sv = re.findall(r'\d{1,2}\s+\w+\s+202[0-9]', r.text)
    print(f'ISO-datum: {dates_iso[:5]}')
    print(f'Svenska datum: {dates_sv[:5]}')
    print(f'Text: {soup.get_text()[:500]}')
except Exception as e:
    print(f'FEL: {e}')

# 2. Epsilon – kolla en träffsida och pagination
print('\n=== EPSILON TRÄFF ===')
r2 = requests.get('https://stud.epsilon.slu.se/11540/', headers=h, timeout=15)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print(f'Status: {r2.status_code}')
print(soup2.get_text()[:400])

# Kolla paginering – hur ser nästa-länk ut?
print('\n=== EPSILON PAGINERING ===')
base_search = 'https://stud.epsilon.slu.se/cgi/search/archive/advanced?screen=Search&exp=0%7C1%7Cyearofpub%2Fcreators_name%2Ftitle%7Carchive%7C-%7Ckeywords%3Akeywords%3AANY%3AEQ%3AMilj%C3%B6+klimat+klimatanpassning+resiliens+naturbaserade+l%C3%B6sningar+dagvatten+ekosystemtj%C3%A4nster+h%C3%A5llbarhet+permakultur+agroforestry+biologisk+m%C3%A5ngfald+kolinlagring+beredskap%7Clanguage%3Alanguage%3AANY%3AEQ%3Aeng+swe&_action_search=S%C3%B6k&cache=14756954&order=yearofpub&reverse=DESC&screen=Search&dataset=archive&start=21'
r3 = requests.get(base_search, headers=h, timeout=20)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
# Hitta träff-tabell
for t in soup3.find_all('table'):
    txt = t.get_text(strip=True)
    if 'Displaying' in txt or len(t.find_all('a', href=True)) > 5:
        for a in t.find_all('a', href=True)[:8]:
            href = a['href']
            txt2 = a.get_text(strip=True)
            if 'epsilon.slu.se/' in href and txt2 and len(txt2) > 5:
                print(f'  {txt2[:80]} | {href[:80]}')
        break