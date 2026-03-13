import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

urls = [
    ('Movium Fakta', 'https://movium.slu.se/soek/?q=movium+fakta'),
    ('Movium Nyheter', 'https://movium.slu.se/nyheter/'),
    ('JBV Webbutik', 'https://webbutiken.jordbruksverket.se/'),
]

for name, url in urls:
    print(f'\n{"="*60}')
    print(f'{name}: {url}')
    try:
        r = requests.get(url, headers=h, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f'Status: {r.status_code}')

        links = soup.find_all('a', href=True)
        print(f'Totalt länkar: {len(links)}')
        for a in links[:6]:
            print(f'  {a.get_text(strip=True)[:60]} | {a["href"][:80]}')

        for tag in ['article', 'h2', 'h3']:
            els = soup.find_all(tag)
            if els:
                print(f'{tag}: {len(els)} st')
                for e in els[:3]:
                    print(f'  {e.get_text(strip=True)[:80]}')

        # Kolla pagination/API
        for s in soup.find_all('script'):
            t = s.string or ''
            if any(x in t.lower() for x in ['api', 'json', 'fetch', 'ajax']) and len(t) > 50:
                print(f'Script: {t[:200]}')
                break
    except Exception as e:
        print(f'FEL: {e}')