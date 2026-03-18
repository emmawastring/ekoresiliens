"""Jordbruksverket Webbutik – KB-scraper för relevanta publikationer"""
import json, requests, re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE      = "Jordbruksverket"
SOURCE_ID   = "jordbruksverket"
KB_FILE     = Path("data/knowledge_resources.json")
BASE_URL    = "https://webbutiken.jordbruksverket.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

# Relevanta kategorisidor med motsvarande KB-kategori
CATEGORIES = [
    ("/sv/artiklar/rapporter/beredskapsfragor-2/index.html",            "beredskap"),
    ("/sv/artiklar/rapporter/beredskapsfragor-2/krisberedskap/index.html", "beredskap"),
    ("/sv/artiklar/rapporter/odling-miljo-och-klimat/index.html",       "klimat"),
    ("/sv/artiklar/rapporter/odling-miljo-och-klimat/klimat/index.html","klimat"),
    ("/sv/artiklar/rapporter/odling-miljo-och-klimat/vatten/index.html","vatten"),
    ("/sv/artiklar/rapporter/odling-miljo-och-klimat/biologisk-mangfald-och-kulturm/index.html", "biodiv"),
    ("/sv/artiklar/rapporter/odling-miljo-och-klimat/odlad-mangfald/index.html", "biodiv"),
    ("/sv/artiklar/rapporter/odling-miljo-och-klimat/energi/index.html","energi"),
    ("/sv/artiklar/rapporter/landsbygdsutveckling/index.html",          "omstallning"),
    ("/sv/artiklar/rapporter/landsbygdsutveckling/mat-och-maltid/index.html", "mat"),
    ("/sv/artiklar/rapporter/handel-marknad-och-konsumente/hallbar-konsumtion-av-jordbruk/index.html", "mat"),
    ("/sv/artiklar/miljo-och-klimat/trycksaker-7/ekologisk-produktion-2/index.html", "mat"),
    ("/sv/artiklar/miljo-och-klimat/trycksaker-7/vatten-och-klimat/index.html", "vatten"),
    ("/sv/artiklar/miljo-och-klimat/trycksaker-7/ett-rikt-odlingslandskap/index.html", "biodiv"),
    ("/sv/artiklar/odling/trycksaker-8/tradgard-2/index.html",          "mat"),
]

def get_publications(path, default_cat):
    url = BASE_URL + path
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        r.encoding = 'iso-8859-1'
        soup = BeautifulSoup(r.text, 'html.parser')
        items = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            title = a.get_text(strip=True)
            # Bara publikationslänkar (ra-nummer eller artiklar med text)
            if not title or len(title) < 8:
                continue
            if not any(x in href for x in ['/sv/artiklar/ra', '/sv/artiklar/ovr', '/sv/artiklar/jo']):
                continue
            full_url = BASE_URL + href if href.startswith('/') else href
            items.append((title, full_url, default_cat))
        return items
    except Exception as e:
        print(f'  FEL {path}: {e}')
        return []

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}
    new_items = []

    for path, cat in CATEGORIES:
        pubs = get_publications(path, cat)
        for title, url, cat in pubs:
            item_id = "jbv_" + re.sub(r'[^a-z0-9]', '_', url.lower())[-50:]
            if item_id in existing_ids:
                continue
            existing_ids.add(item_id)
            new_items.append({
                "id":          item_id,
                "source":      SOURCE,
                "source_name": SOURCE,
                "type":        "rapport",
                "icon":        "🌾",
                "title":       title,
                "desc":        "",
                "cats":        [cat],
                "url":         url,
                "year":        2024,
            })
            print(f"  + {title[:70]}")

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKlar! Lade till {len(new_items)} poster.")