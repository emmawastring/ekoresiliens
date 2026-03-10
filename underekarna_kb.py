"""Under Ekarna – KB-scraper (Förädling + Historia)"""
import json, requests
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE      = "Under Ekarna"
SOURCE_ID   = "underekarna"
KB_FILE     = Path("data/knowledge_resources.json")
HEADERS     = {"User-Agent": "Mozilla/5.0"}
BASE_URL    = "https://www.underekarna.se"

PAGES = [
    {
        "url":   f"{BASE_URL}/f%C3%B6r%C3%A4dling/",
        "id":    "underekarna_foradling",
        "title": "Förädling av ekollon – guide",
        "cats":  ["skog", "mat", "beredskap", "agroforestry"],
        "type":  "guide",
    },
    {
        "url":   f"{BASE_URL}/historia/",
        "id":    "underekarna_historia",
        "title": "Ekollon och balanokultur – historia",
        "cats":  ["skog", "mat", "agroforestry"],
        "type":  "artikel",
    },
]

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}
    new_items = []

    for page in PAGES:
        if page["id"] in existing_ids:
            print(f"  Redan finns: {page['id']}")
            continue
        try:
            r = requests.get(page["url"], headers=HEADERS, timeout=15)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            main = soup.find("main") or soup.find("body")
            desc = main.get_text(" ", strip=True)[:300] if main else ""

            new_items.append({
                "id":          page["id"],
                "source":      SOURCE,
                "source_name": SOURCE,
                "type":        page["type"],
                "icon":        "🌳",
                "title":       page["title"],
                "desc":        desc,
                "cats":        page["cats"],
                "url":         page["url"],
                "year":        2024,
            })
            print(f"  Lade till: {page['title']}")
        except Exception as e:
            print(f"  Fel: {page['url']}: {e}")

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Klar! Lade till {len(new_items)} poster.")