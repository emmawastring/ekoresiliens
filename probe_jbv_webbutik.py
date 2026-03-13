import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# JBV webbutik - kolla kategorisidor
for url in [
    'https://webbutiken.jordbruksverket.se/sv/artiklar/om-jordbruksverket/index.html',
    'https://webbutiken.jordbruksverket.se/sv/',
]:
    print(f'\n== {url} ==')
    try:
        r = requests.get(url, headers=h, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f'Status: {r.status_code}')
        # Nav/meny-struktur
        nav = soup.find(['nav', 'ul'], class_=re.compile(r'nav|menu|cat', re.I))
        if nav:
            for a in nav.find_all('a', href=True)[:15]:
                print(f'  {a.get_text(strip=True)[:60]} | {a["href"][:80]}')
        # Alla länkar
        for a in soup.find_all('a', href=True)[:20]:
            txt = a.get_text(strip=True)
            if txt and len(txt) > 3:
                print(f'  {txt[:60]} | {a["href"][:80]}')
    except Exception as e:
        print(f'FEL: {e}')