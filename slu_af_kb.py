"""SLU nyheter + Agroforestry.se KB-scraper"""
import json, requests, re
from pathlib import Path
from bs4 import BeautifulSoup

KB_FILE = Path("data/knowledge_resources.json")
HEADERS = {"User-Agent": "Mozilla/5.0"}

# === SLU nyheter ===
def fetch_slu_news():
    items = []
    seen = set()
    for page_url in [
        'https://www.slu.se/kalender/',
        'https://www.slu.se/nyheter/',
    ]:
        try:
            r = requests.get(page_url, headers=HEADERS, timeout=15)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            for hit in soup.select('.search-hit'):
                title_el = hit.select_one('.search-hit__title a')
                date_el  = hit.select_one('.search-hit__metainfo')
                if not title_el:
                    continue
                url   = title_el.get('href', '')
                title = title_el.get_text(strip=True)
                date  = date_el.get_text(strip=True) if date_el else ''
                year  = int(date[:4]) if re.match(r'\d{4}', date) else 2026
                if url in seen:
                    continue
                seen.add(url)
                item_id = 'slu_news_' + re.sub(r'[^a-z0-9]', '_', url.lower())[-40:]
                items.append({
                    'id':          item_id,
                    'source':      'SLU',
                    'source_name': 'Sveriges lantbruksuniversitet',
                    'type':        'artikel',
                    'icon':        '🌱',
                    'title':       title,
                    'desc':        '',
                    'cats':        ['omstallning', 'biodiv', 'mat'],
                    'url':         url,
                    'year':        year,
                })
        except Exception as e:
            print(f'SLU fel: {e}')
    return items

# === Agroforestry.se ===
AF_PAGES = [
    ('https://agroforestry.se/2-tradjordbruk/',           'Alléodling och trädjordbruk',      ['agroforestry', 'mat', 'skog']),
    ('https://agroforestry.se/5-kantzon-odling/',         'Kantzonodling',                     ['agroforestry', 'biodiv']),
    ('https://agroforestry.se/4-skogsodling/',            'Skogsodling',                       ['agroforestry', 'skog', 'mat']),
    ('https://agroforestry.se/3-skogsbete/',              'Skogsbete och betesskogsbruk',      ['agroforestry', 'skog']),
    ('https://agroforestry.se/olika-agroforestrysystem/', 'Fördelar med agroforestry',         ['agroforestry']),
    ('https://agroforestry.se/om-agroforestry-sverige/',  'Om Agroforestry Sverige',           ['agroforestry']),
    ('https://agroforestry.se/vanliga-fragor-om-regler-och-stod-for-agroforestry-i-sverige/', 'Regler och stöd för agroforestry i Sverige', ['agroforestry', 'policy']),
]

def fetch_af_kb():
    items = []
    for url, title, cats in AF_PAGES:
        item_id = 'agroforestry_' + url.split('/')[-2].replace('-', '_')
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            r.encoding = 'utf-8'
            soup = BeautifulSoup(r.text, 'html.parser')
            main = soup.find('main') or soup.find('article') or soup.find('body')
            desc = main.get_text(' ', strip=True)[:300] if main else ''
        except:
            desc = ''
        items.append({
            'id':          item_id,
            'source':      'Agroforestry Sverige',
            'source_name': 'Agroforestry Sverige',
            'type':        'guide',
            'icon':        '🌳',
            'title':       title,
            'desc':        desc,
            'cats':        cats,
            'url':         url,
            'year':        2024,
        })
    return items

if __name__ == '__main__':
    existing = json.loads(KB_FILE.read_text(encoding='utf-8'))
    existing_ids = {e['id'] for e in existing}

    new_items = []
    for item in fetch_slu_news() + fetch_af_kb():
        if item['id'] not in existing_ids:
            new_items.append(item)
            print(f'  + {item["source"]}: {item["title"][:60]}')

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f'\nKlar! Lade till {len(new_items)} poster.')