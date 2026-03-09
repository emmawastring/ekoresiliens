"""
Försöker hämta publiceringsdatum för alla poster i knowledge_resources.json
via meta-taggar. Sparar year-fält på de som hittas.
"""
import json, re, time
import requests
from bs4 import BeautifulSoup

HEADERS = {'User-Agent': 'Mozilla/5.0 (compatible; EkoresiliensBot/1.0)'}
TIMEOUT = 8

DATE_METAS = [
    {'property': 'article:published_time'},
    {'name': 'article:published_time'},
    {'property': 'og:updated_time'},
    {'name': 'pubdate'},
    {'name': 'date'},
    {'name': 'DC.date'},
    {'name': 'DC.Date'},
    {'itemprop': 'datePublished'},
]

def extract_year(soup):
    # 1. Meta-taggar
    for attrs in DATE_METAS:
        tag = soup.find('meta', attrs=attrs)
        if tag:
            val = tag.get('content', '')
            m = re.search(r'(20\d{2})', val)
            if m:
                return int(m.group(1))

    # 2. JSON-LD
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string or '')
            for key in ['datePublished', 'dateModified', 'dateCreated']:
                if key in data:
                    m = re.search(r'(20\d{2})', str(data[key]))
                    if m:
                        return int(m.group(1))
        except Exception:
            pass

    # 3. time[datetime] element
    tag = soup.find('time', datetime=True)
    if tag:
        m = re.search(r'(20\d{2})', tag['datetime'])
        if m:
            return int(m.group(1))

    return None

data = json.load(open('data/knowledge_resources.json', encoding='utf-8'))

found = 0
skipped = 0

for i, item in enumerate(data):
    if item.get('year'):
        print(f"  [{i+1}/{len(data)}] Redan har år: {item['title'][:40]} → {item['year']}")
        skipped += 1
        continue

    url = item.get('url', '')
    if not url:
        continue

    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True)
        soup = BeautifulSoup(r.text, 'html.parser')
        year = extract_year(soup)
        if year:
            item['year'] = year
            found += 1
            print(f"  [{i+1}/{len(data)}] ✓ {item['title'][:40]} → {year}")
        else:
            print(f"  [{i+1}/{len(data)}] – Inget datum: {item['title'][:40]}")
        time.sleep(0.5)
    except Exception as e:
        print(f"  [{i+1}/{len(data)}] FEL {item['title'][:40]}: {e}")

json.dump(data, open('data/knowledge_resources.json', 'w', encoding='utf-8'),
          ensure_ascii=False, indent=2)

print(f"\nKlar! Hittade år för {found} poster, {skipped} hade redan år.")