"""
Hushållningssällskapet – kunskapsbank-scraper.
Hämtar press-meddelanden och artiklar via WP REST API och lägger dem i knowledge_resources.json.
"""
import json, requests
from pathlib import Path
from bs4 import BeautifulSoup

SOURCE      = "Hushållningssällskapet"
SOURCE_ID   = "hushallningssallskapet"
KB_FILE     = Path("data/knowledge_resources.json")
HEADERS     = {"User-Agent": "Mozilla/5.0"}

CATEGORY_KEYWORDS = {
    "klimat":       ["klimat", "väder", "temperatur", "koldioxid", "utsläpp", "fossil"],
    "biodiv":       ["biologisk mångfald", "arter", "pollinator", "insekt", "naturvård"],
    "mat":          ["livsmedel", "jordbruk", "odling", "lantbruk", "grönsak", "mjölk", "kött", "spannmål"],
    "skog":         ["skog", "skogsbruk", "timber", "virke", "träd"],
    "vatten":       ["vatten", "bevattning", "dikesrensning", "grundvatten", "sjö", "å"],
    "energi":       ["energi", "biogas", "sol", "vind", "förnybar"],
    "samhalle":     ["landsbygd", "bygd", "lokal", "regional", "hushållning"],
    "agroforestry": ["agroforestry", "skogsträdgård", "silvopasture"],
}

def guess_cats(text):
    text = text.lower()
    cats = []
    for cat, kws in CATEGORY_KEYWORDS.items():
        if any(kw in text for kw in kws):
            cats.append(cat)
    return cats or ["samhalle"]

def fetch_items(endpoint, type_label, icon):
    items = []
    page = 1
    while True:
        r = requests.get(
            f"https://hushallningssallskapet.se/wp-json/wp/v2/{endpoint}",
            params={"per_page": 50, "page": page, "status": "publish",
                    "_fields": "id,date,title,link,content,excerpt"},
            headers=HEADERS, timeout=15
        )
        if r.status_code in (400, 404):
            break
        r.raise_for_status()
        data = r.json()
        if not data:
            break
        for item in data:
            title = BeautifulSoup(item["title"]["rendered"], "html.parser").get_text()
            desc  = BeautifulSoup(
                item.get("excerpt", {}).get("rendered", "") or
                item.get("content", {}).get("rendered", ""), "html.parser"
            ).get_text(" ", strip=True)[:300]
            year  = item["date"][:4]
            cats  = guess_cats(title + " " + desc)
            items.append({
                "id":          f"{SOURCE_ID}_{endpoint}_{item['id']}",
                "source":      SOURCE,
                "source_name": SOURCE,
                "type":        type_label,
                "icon":        icon,
                "title":       title,
                "desc":        desc,
                "cats":        cats,
                "url":         item["link"],
                "year":        int(year),
            })
        page += 1
    return items

if __name__ == "__main__":
    existing = json.loads(KB_FILE.read_text(encoding="utf-8"))
    existing_ids = {e["id"] for e in existing}

    new_items = []
    for endpoint, type_label, icon in [
        ("press", "artikel", "📰"),
        ("posts", "artikel", "📄"),
    ]:
        fetched = fetch_items(endpoint, type_label, icon)
        added = [x for x in fetched if x["id"] not in existing_ids]
        print(f"  {endpoint}: {len(fetched)} hämtade, {len(added)} nya")
        new_items.extend(added)

    existing.extend(new_items)
    KB_FILE.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nKlar! Lade till {len(new_items)} poster i {KB_FILE}")