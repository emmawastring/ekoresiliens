"""Skogsstyrelsen – KB-scraper för rapporter"""
import json, requests, re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE      = "Skogsstyrelsen"
SOURCE_ID   = "skogsstyrelsen"
KB_FILE     = Path("data/knowledge_resources.json")
BASE_URL    = "https://www.skogsstyrelsen.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

CATEGORY_KEYWORDS = {
    "klimat":       ["klimat", "koldioxid", "kolsänka", "utsläpp", "klimatanpassning"],
    "biodiv":       ["biologisk mångfald", "nyckelbiotop", "artskydd", "naturvård", "biotopskydd"],
    "skog":         ["skog", "skogsbruk", "avverkning", "hyggesfritt", "föryngring", "virke"],
    "vatten":       ["vatten", "dikad", "återvätning", "torvmark"],
    "energi":       ["bioenergi", "biobränsle", "energi"],
    "policy":       ["policy", "direktiv", "lagstiftning", "föreskrift", "regelförenkling", "regeringsuppdrag"],
    "omstallning":  ["omvärldsanalys", "hållbar", "omställning", "social"],
}

def guess_cats(text):
    text = text.lower()
    cats = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in kws):
            cats.append(cat)
    return cats or ["skog"]

def extract_year(title, href):
    m = re.search(r'20(\d{2})', title)
    if m:
        return int("20" + m.group(1))
    m2 = re.search(r'rapporter-(\d{4})', href)
    if m2:
        return int(m2.group(1))
    return 2023

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}

    r = requests.get(
        f"{BASE_URL}/om-oss/rapporter-bocker-och-broschyrer/",
        headers=HEADERS, timeout=15
    )
    r.encoding = "utf-8"
    soup = BeautifulSoup(r.text, "html.parser")

    new_items = []
    for a in soup.find_all("a", href=True):
        href = a["href"]
        title = a.get_text(strip=True)

        # Bara PDF-rapporter från globalassets
        if "globalassets" not in href or not title.startswith("Rapport"):
            continue

        # Hoppa över äldre än 2020
        year = extract_year(title, href)
        if year < 2020:
            continue

        # Rensa titel från filstorlek
        clean_title = re.sub(r'\.pdf.*$', '', title).strip()

        url = href if href.startswith("http") else BASE_URL + href
        item_id = "sks_" + re.sub(r'[^a-z0-9]', '_', href.lower())[-50:]

        if item_id in existing_ids:
            continue

        cats = guess_cats(clean_title)
        new_items.append({
            "id":          item_id,
            "source":      SOURCE,
            "source_name": SOURCE,
            "type":        "rapport",
            "icon":        "🌲",
            "title":       clean_title,
            "desc":        "",
            "cats":        cats,
            "url":         url,
            "year":        year,
        })

    print(f"  {len(new_items)} nya rapporter")
    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Klar! Lade till {len(new_items)} poster.")