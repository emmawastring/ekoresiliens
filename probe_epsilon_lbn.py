import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# 1. SLU Epsilon
print('='*60)
print('SLU EPSILON')
url = 'https://stud.epsilon.slu.se/cgi/search/archive/advanced?dataset=archive&screen=Search&documents_merge=ALL&documents=&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&abstract_merge=ALL&abstract=&date=&series_merge=ALL&series=&keywords_merge=ANY&keywords=Milj%C3%B6%2C+klimat+%2C+klimatanpassning%2C+resiliens%2C+stadsplanering%2C+perenn%2C+naturbaserade+l%C3%B6sningar%2C+dagvatten%2C+skyfall%2C+ekosystemtj%C3%A4nster%2C+h%C3%A5llbarhet%2C+cirkul%C3%A4ritet&language=eng&language=swe&divisions_merge=ANY&examiner_name_merge=ALL&examiner_name=&supervisor_name_merge=ALL&supervisor_name=&coursecode_merge=ALL&coursecode=&subjects_merge=ANY&yearofpub=&program_merge=ANY&stakeholders_merge=ANY&earchived=EITHER&eadate=&eacomment_merge=ALL&eacomment=&course_code_merge=ALL&course_code=&course_resp_dept_sv_merge=ALL&course_resp_dept_sv=&course_resp_dept_oid_merge=ALL&course_resp_dept_oid=&satisfyall=ALL&order=yearofpub%2Fcreators_name%2Ftitle&_action_search=S%C3%B6k'
r = requests.get(url, headers=h, timeout=20)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print(f'Status: {r.status_code}')
# Eprints typisk struktur
for a in soup.find_all('a', href=True):
    href = a['href']
    txt = a.get_text(strip=True)
    if '/id/eprint/' in href and txt and len(txt) > 10:
        print(f'  {txt[:80]} | {href[:80]}')
        break
# Räkna träffar
eprint_links = [a for a in soup.find_all('a', href=True) if '/id/eprint/' in a['href']]
print(f'Eprint-länkar: {len(eprint_links)}')
for a in eprint_links[:5]:
    print(f'  {a.get_text(strip=True)[:80]}')
# Sidbrytning?
pages = soup.find_all('a', href=True, string=re.compile(r'^\d+$'))
print(f'Sidlänkar: {[a.get_text() for a in pages[:10]]}')
# År-info
years = re.findall(r'(202[0-9]|201[5-9])', soup.get_text())
print(f'År i texten: {set(years)}')
print('Textexcerpt:', soup.get_text()[:300])

# 2. Landsbygdsnätverket
print('\n' + '='*60)
print('LANDSBYGDSNÄTVERKET')
url2 = 'https://www.landsbygdsnatverket.se/hallbaragronanaringar.4.28dc3ce718e0c90ff2710025.html'
r2 = requests.get(url2, headers=h, timeout=15)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print(f'Status: {r2.status_code}')
dates = re.findall(r'202[0-9]-\d{2}-\d{2}', r2.text)
print(f'ISO-datum: {dates[:5]}')
dates_sv = re.findall(r'\d{1,2}\s+\w+\s+202[0-9]', r2.text)
print(f'Svenska datum: {dates_sv[:5]}')
links = soup2.find_all('a', href=True)
print(f'Totalt länkar: {len(links)}')
for a in links[:10]:
    txt = a.get_text(strip=True)
    if txt and len(txt) > 5:
        print(f'  {txt[:70]} | {a["href"][:80]}')
for tag in ['article','h2','h3']:
    els = soup2.find_all(tag)
    if els:
        print(f'{tag}: {len(els)} st')
        for e in els[:3]: print(f'  {e.get_text(strip=True)[:80]}')
print('Text:', soup2.get_text()[:400])