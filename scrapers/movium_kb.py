"""Movium KB-scraper – Fakta-PDF:er och nyheter"""
import json, requests, re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE      = "Movium"
SOURCE_ID   = "movium"
KB_FILE     = Path("data/knowledge_resources.json")
BASE_URL    = "https://movium.slu.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

CATEGORY_KEYWORDS = {
    "klimat":       ["klimat", "koldioxid", "torka", "värme", "dagvatten", "regnbädd"],
    "biodiv":       ["biologisk mångfald", "pollinator", "insekt", "invasiv", "art", "ekologi", "vilt"],
    "skog":         ["träd", "skog", "urban skog", "skötsel av träd", "beskärning"],
    "vatten":       ["vatten", "dagvatten", "regnbädd", "översvämning"],
    "mat":          ["odla", "odling", "skolgård", "lekplats"],
    "omstallning":  ["grön", "hållbar", "stadsplanering", "utemiljö", "park", "landskap"],
}

def guess_cats(text):
    text = text.lower()
    cats = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in kws):
            cats.append(cat)
    return cats or ["omstallning"]

def extract_year(text, href):
    m = re.search(r'(20\d{2})', text)
    if m:
        return int(m.group(1))
    m2 = re.search(r'(20\d{2})', href)
    if m2:
        return int(m2.group(1))
    return 2023

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}
    new_items = []

    # 1. Movium Fakta PDF:er
    print("Hämtar Movium Fakta...")
    r = requests.get(f"{BASE_URL}/soek/?q=movium+fakta", headers=HEADERS, timeout=15)
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/media/" not in href or ".pdf" not in href.lower():
            continue
        # Titel från parent h2 eller länktext
        h2 = a.find_parent("h2") or a.find_parent("li") or a
        raw_title = h2.get_text(" ", strip=True)
        # Rensa "Nyheter / " prefix och "PDF: ..." suffix
        title = re.sub(r'^.*?Movium Fakta', 'Movium Fakta', raw_title)
        title = re.sub(r'PDF:.*$', '', title).strip()
        if not title or "Movium Fakta" not in title:
            continue

        url = href if href.startswith("http") else BASE_URL + href
        item_id = "movium_fakta_" + re.sub(r'[^a-z0-9]', '_', href.lower())[-40:]

        if item_id in existing_ids:
            continue

        year = extract_year(title, href)
        cats = guess_cats(title)
        new_items.append({
            "id":          item_id,
            "source":      SOURCE,
            "source_name": SOURCE,
            "type":        "rapport",
            "icon":        "🌿",
            "title":       title,
            "desc":        "",
            "cats":        cats,
            "url":         url,
            "year":        year,
        })
        print(f"  + {title[:70]}")

    # 2. Movium Nyheter
    print("\nHämtar Movium Nyheter...")
    r2 = requests.get(f"{BASE_URL}/nyheter/", headers=HEADERS, timeout=15)
    r2.encoding = "utf-8"
    soup2 = BeautifulSoup(r2.text, "html.parser")

    for a in soup2.find_all("a", href=True):
        href = a["href"]
        if "/nyheter/" not in href or href == "/nyheter/":
            continue
        title = a.get_text(strip=True)
        if not title or len(title) < 10:
            continue
        url = href if href.startswith("http") else BASE_URL + href
        item_id = "movium_nyhet_" + re.sub(r'[^a-z0-9]', '_', href.lower())[-40:]
        if item_id in existing_ids:
            continue
        year = extract_year(href, href)
        cats = guess_cats(title)
        new_items.append({
            "id":          item_id,
            "source":      SOURCE,
            "source_name": SOURCE,
            "type":        "artikel",
            "icon":        "🌿",
            "title":       title,
            "desc":        "",
            "cats":        cats,
            "url":         url,
            "year":        year,
        })
        print(f"  + {title[:70]}")

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKlar! Lade till {len(new_items)} poster.")