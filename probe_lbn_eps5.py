import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

BASE_LBN = 'https://www.landsbygdsnatverket.se'

# 1. LBN – hämta alla fullständiga event-länkarna
print('=== LBN ALLA EVENT-LÄNKAR ===')
r = requests.get(BASE_LBN + '/kommandeaktiviteter.4.490b482015189b53667216b.html', headers=h, timeout=15)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
for a in soup.find_all('a', href=True):
    href = a['href']
    if 'kalenderaktiviteter' in href:
        full = BASE_LBN + href if href.startswith('/') else href
        print(f'  {a.get_text(strip=True)[:60]} | {full}')

# 2. Epsilon – hämta träfftabell korrekt med cache-URL från sidan
print('\n=== EPSILON TRÄFFTABELL ===')
search_url = 'https://stud.epsilon.slu.se/cgi/search/archive/advanced?dataset=archive&screen=Search&keywords_merge=ANY&keywords=klimatanpassning+resiliens+naturbaserade+dagvatten+ekosystemtj%C3%A4nster+h%C3%A5llbarhet+permakultur+agroforestry+biologisk+m%C3%A5ngfald+kolinlagring+beredskap+livsmedel&language=swe&satisfyall=ALL&order=yearofpub&reverse=DESC&_action_search=S%C3%B6k'
r2 = requests.get(search_url, headers=h, timeout=20)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
# Hitta tabell med träffar
for t in soup2.find_all('table'):
    links = [a for a in t.find_all('a', href=True) if 'stud.epsilon.slu.se/' in a.get('href','') and re.search(r'/\d+/', a['href'])]
    if links:
        print(f'Hittade träfftabell med {len(links)} länkar')
        for a in links[:10]:
            yr_match = re.search(r'(20\d{2})', t.get_text())
            print(f'  {a.get_text(strip=True)[:80]} | {a["href"]}')
        break
# Kolla räknar-text
count_text = re.search(r'Displaying results.*?of\s*(\d+)', soup2.get_text())
if count_text:
    print(f'\nTotalt träffar: {count_text.group(0)}')