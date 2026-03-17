import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# 1. Epsilon – kolla vad som faktiskt finns i HTML
print('=== EPSILON HTML-STRUKTUR ===')
url = 'https://stud.epsilon.slu.se/cgi/search/archive/advanced?dataset=archive&screen=Search&documents_merge=ALL&documents=&title_merge=ALL&title=&creators_name_merge=ALL&creators_name=&abstract_merge=ALL&abstract=&date=&series_merge=ALL&series=&keywords_merge=ANY&keywords=Milj%C3%B6%2C+klimat+%2C+klimatanpassning%2C+resiliens%2C+stadsplanering%2C+perenn%2C+naturbaserade+l%C3%B6sningar%2C+dagvatten%2C+skyfall%2C+ekosystemtj%C3%A4nster%2C+h%C3%A5llbarhet%2C+cirkul%C3%A4ritet%2C+permakultur%2C+skogstr%C3%A4dg%C3%A5rd%2C+agroforestry%2C+biologisk+m%C3%A5ngfald%2C+%C3%A5terv%C3%A4tning%2C+kolinlagring%2C+livsmedels%2C+beredskap&language=eng&language=swe&satisfyall=ALL&order=yearofpub%2Fcreators_name%2Ftitle&_action_search=S%C3%B6k'
r = requests.get(url, headers=h, timeout=20)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')

# Hitta alla länkar
all_links = soup.find_all('a', href=True)
print(f'Totalt länkar: {len(all_links)}')
# Kolla epsilon-domänlänkar
for a in all_links[:30]:
    href = a['href']
    txt = a.get_text(strip=True)
    if txt and len(txt) > 8 and not any(x in href for x in ['css','js','logo','search','#']):
        print(f'  {txt[:80]} | {href[:80]}')

# Kolla om det finns listor med träffar
for tag in ['ol','ul','table']:
    els = soup.find_all(tag)
    if els:
        print(f'\n{tag}: {len(els)} st')
        for e in els[:2]:
            print(e.get_text(strip=True)[:200])

# 2. Landsbygdsnätverket – kommande aktiviteter och nyheter
print('\n=== LBN KOMMANDE AKTIVITETER ===')
r2 = requests.get('https://www.landsbygdsnatverket.se/kommandeaktiviteter.4.490b482015189b53667216b.html', headers=h, timeout=15)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print(f'Status: {r2.status_code}')
dates = re.findall(r'202[0-9]-\d{2}-\d{2}', r2.text)
print(f'ISO-datum: {dates[:5]}')
for tag in ['article','h2','h3','h4']:
    els = soup2.find_all(tag)
    if els:
        print(f'{tag}: {len(els)} st')
        for e in els[:3]: print(f'  {e.get_text(strip=True)[:80]}')
for a in soup2.find_all('a', href=True)[:10]:
    txt = a.get_text(strip=True)
    if txt and len(txt) > 5:
        print(f'  {txt[:70]} | {a["href"][:80]}')

print('\n=== LBN NYHETER ===')
r3 = requests.get('https://www.landsbygdsnatverket.se/nyheterochartiklar.4.6450369c15213cd6fe7e0b1d.html', headers=h, timeout=15)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
print(f'Status: {r3.status_code}')
for tag in ['article','h2','h3']:
    els = soup3.find_all(tag)
    if els:
        print(f'{tag}: {len(els)} st')
        for e in els[:3]: print(f'  {e.get_text(strip=True)[:80]}')
print(soup3.get_text()[:400])