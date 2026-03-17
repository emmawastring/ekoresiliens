"""SLU Epsilon – KB-scraper för studentuppsatser"""
import json, requests, re
from pathlib import Path
from bs4 import BeautifulSoup
import time

SOURCE      = "SLU Epsilon"
SOURCE_ID   = "epsilon"
KB_FILE     = Path("data/knowledge_resources.json")
BASE_URL    = "https://stud.epsilon.slu.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

# Sökord – utökade
KEYWORDS = (
    "klimatanpassning resiliens naturbaserade+lösningar dagvatten ekosystemtjänster "
    "hållbarhet permakultur agroforestry biologisk+mångfald kolinlagring beredskap "
    "livsmedelsförsörjning skogsträdgård återvätning klimat jordbruk landsbygd "
    "självhushållning omställning permaculture food+security"
)

SEARCH_URL = (
    "https://stud.epsilon.slu.se/cgi/search/archive/advanced"
    "?dataset=archive&screen=Search"
    "&keywords_merge=ANY&keywords=" + KEYWORDS.replace(' ', '+')
    + "&language=swe&language=eng"
    "&satisfyall=ALL&order=yearofpub&reverse=DESC"
    "&_action_search=Sök"
)

def guess_cats(title):
    t = title.lower()
    cats = []
    if any(x in t for x in ['klimat', 'temperatur', 'koldioxid', 'co2']): cats.append('klimat')
    if any(x in t for x in ['biologisk mångfald', 'arter', 'habitat', 'ekosystem']): cats.append('biodiv')
    if any(x in t for x in ['skog', 'träd', 'skogsbruk']): cats.append('skog')
    if any(x in t for x in ['vatten', 'dagvatten', 'våtmark', 'skyfall']): cats.append('vatten')
    if any(x in t for x in ['mat', 'livsmedel', 'jordbruk', 'odling', 'lantbruk']): cats.append('mat')
    if any(x in t for x in ['energi', 'biogas', 'förnybar']): cats.append('energi')
    if any(x in t for x in ['permakultur', 'skogsträdgård', 'agroforestry']): cats.append('skogstradgard')
    if any(x in t for x in ['beredskap', 'resiliens', 'sårbarhet']): cats.append('beredskap')
    return cats or ['omstallning']

def scrape_page(url):
    r = requests.get(url, headers=HEADERS, timeout=20)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    items = []
    for t in soup.find_all('table'):
        links = [a for a in t.find_all('a', href=True)
                 if re.search(r'stud\.epsilon\.slu\.se/\d+', a['href'])]
        if not links:
            continue
        # Hämta år från omgivande text
        rows = t.find_all('tr')
        for row in rows:
            a = row.find('a', href=re.compile(r'/\d+/$'))
            if not a:
                continue
            title = a.get_text(strip=True)
            href = a['href']
            url_item = href if href.startswith('http') else BASE_URL + href
            # År från radtexten
            row_text = row.get_text()
            yr_m = re.search(r'(20[01]\d|19\d\d)', row_text)
            year = int(yr_m.group(1)) if yr_m else 2020
            items.append((title, url_item, year))
        break
    return items

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}
    new_items = []

    # Hämta max 10 sidor (200 träffar) – de nyaste
    for page in range(10):
        start = page * 20
        url = SEARCH_URL + (f'&start={start}' if start > 0 else '')
        print(f'Sida {page+1} (start={start})...')
        try:
            results = scrape_page(url)
            if not results:
                print('  Inga träffar, avbryter')
                break
            for title, item_url, year in results:
                if year < 2018:
                    continue
                item_id = "epsilon_" + re.sub(r'[^a-z0-9]', '_', item_url.lower())[-30:]
                if item_id in existing_ids:
                    continue
                existing_ids.add(item_id)
                cats = guess_cats(title)
                new_items.append({
                    "id":          item_id,
                    "source":      SOURCE,
                    "source_name": SOURCE,
                    "type":        "rapport",
                    "icon":        "🎓",
                    "title":       title,
                    "desc":        "",
                    "cats":        cats,
                    "url":         item_url,
                    "year":        year,
                })
                print(f'  + [{year}] {title[:70]}')
            time.sleep(0.5)
        except Exception as e:
            print(f'  FEL: {e}')
            break

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKlar! Lade till {len(new_items)} poster.")