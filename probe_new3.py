import requests, re
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

urls = [
    ('Jordbruksverket', 'https://jordbruksverket.se/om-jordbruksverket/kurser-och-seminarier'),
    ('SvenskKolinlagring', 'https://svenskkolinlagring.se/kalendarium/'),
    ('SV Trädgård', 'https://www.sv.se/kurser-och-evenemang/tradgard-hus-och-hem/tradgard'),
]

for name, url in urls:
    print(f'\n{"="*60}')
    print(f'{name}: {url}')
    try:
        r = requests.get(url, headers=h, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')
        print(f'Status: {r.status_code}')

        # Datum
        dates = re.findall(r'202[5-9]-\d{2}-\d{2}', r.text)
        print(f'Datum (ISO): {dates[:5]}')
        dates_sv = re.findall(r'\d{1,2}\s+(?:jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec)\w*\s+202[5-9]', r.text, re.I)
        print(f'Datum (sv): {dates_sv[:5]}')

        # Kolla script-taggar
        for s in soup.find_all('script'):
            t = s.string or ''
            if any(x in t.lower() for x in ['event', 'kurs', 'datum', 'date', 'calendar']) and len(t) > 100:
                print(f'Script med data: {t[:300]}')
                print('---')

        # Kolla länk-struktur
        links = soup.find_all('a', href=True)
        event_links = [a for a in links if any(x in (a.get('href','') + a.get_text()).lower() for x in ['kurs', 'event', 'seminar', 'webinar', 'kalend'])]
        print(f'Event-liknande länkar: {len(event_links)}')
        for a in event_links[:3]:
            print(f'  {a.get_text(strip=True)[:60]} | {a["href"][:70]}')

        # Main-text
        main = soup.find('main') or soup.find('body')
        if main:
            print(f'Text: {main.get_text()[:400]}')
    except Exception as e:
        print(f'FEL: {e}')