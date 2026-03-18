"""RUS – KB-scraper för publikationer och nyheter"""
import json, requests, re
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE      = "RUS Miljömål"
KB_FILE     = Path("data/knowledge_resources.json")
BASE_URL    = "https://www.rus.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

PAGES = [
    ("https://www.rus.se/category/publikationer/", "klimat"),
    ("https://www.rus.se/category/nyheter/",       "omstallning"),
    ("https://www.rus.se/stod-i-atgardsarbetet/",  "biodiv"),
]

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}
    new_items = []

    for page_url, cat in PAGES:
        r = requests.get(page_url, headers=HEADERS, timeout=15)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a", href=True):
            href = a["href"]
            title = a.get_text(strip=True)
            if not title or len(title) < 10:
                continue
            if "rus.se" not in href:
                continue
            if any(x in href for x in ["category", "stod-i-atgardsarbetet", "#", "nyhetsbrev", "kontakta", "om-rus", "english", "statistik", "miljomalsradet", "regional-arlig"]):
                continue

            url = href if href.startswith("http") else BASE_URL + href
            item_id = "rus_" + re.sub(r"[^a-z0-9]", "_", url.lower())[-50:]
            if item_id in existing_ids:
                continue
            existing_ids.add(item_id)

            yr = re.search(r"(20\d{2})", url)
            year = int(yr.group(1)) if yr else 2024

            new_items.append({
                "id":          item_id,
                "source":      SOURCE,
                "source_name": SOURCE,
                "type":        "artikel",
                "icon":        "🎯",
                "title":       title,
                "desc":        "",
                "cats":        [cat],
                "url":         url,
                "year":        year,
            })
            print(f"  + {title[:70]}")

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKlar! Lade till {len(new_items)} poster.")