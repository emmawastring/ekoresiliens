"""Naturvårdsverket – hämtar via sökresultat JSON"""
import requests
import re
import json
from bs4 import BeautifulSoup
from .base import BaseScraper

SOURCE_NAME = "Naturvårdsverket"
BASE_URL    = "https://www.naturvardsverket.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

MONTHS = {
    "januari":1,"februari":2,"mars":3,"april":4,"maj":5,"juni":6,
    "juli":7,"augusti":8,"september":9,"oktober":10,"november":11,"december":12
}

def url_to_date(url):
    m = re.search(r'/kalendarium/(\d{4})/([a-z]+)/', url)
    if m:
        year = int(m.group(1))
        month = MONTHS.get(m.group(2).lower())
        if month:
            return f"{year}-{month:02d}-01"
    return None

def extract_model(html):
    soup = BeautifulSoup(html, "html.parser")
    for s in soup.find_all("script"):
        t = s.string or ""
        if "window.__model" in t:
            m = re.search(r"window\.__model\s*=\s*(\{.+\})\s*;?\s*$", t, re.DOTALL)
            if m:
                try:
                    return json.loads(m.group(1))
                except:
                    pass
    return None

class NaturvardsverketScraper(BaseScraper):
    name      = SOURCE_NAME
    source_id = "naturvardsverket"

    def fetch(self) -> list[dict]:
        events = []
        seen = set()

        for search_term in ["evenemang", "webbinarium", "kurs", "seminarium"]:
            page = 1
            while True:
                url = f"{BASE_URL}/soksida/?q={search_term}&p={page}"
                try:
                    r = requests.get(url, headers=HEADERS, timeout=15)
                    r.raise_for_status()
                    model = extract_model(r.text)
                    if not model:
                        break

                    results = (model.get("content", {})
                                    .get("searchModel", {})
                                    .get("results", []))
                    if not results:
                        break

                    found_new = False
                    for item in results:
                        item_url = item.get("url", "")
                        if "/kalendarium/" not in item_url:
                            continue
                        if item_url in seen:
                            continue
                        seen.add(item_url)

                        date_iso = url_to_date(item_url)
                        if not date_iso:
                            continue

                        title = item.get("heading", "").strip()
                        desc  = item.get("excerpt", "").strip()

                        events.append(self.event(
                            title=title,
                            date_iso=date_iso,
                            url=item_url,
                            description=desc,
                            categories=["omstallning", "klimat", "biodiv"],
                        ))
                        found_new = True

                    total_pages = (model.get("content", {})
                                        .get("searchModel", {})
                                        .get("totalPages", 1))
                    if not found_new or page >= total_pages:
                        break
                    page += 1

                except Exception as e:
                    print(f"  {SOURCE_NAME}: fel ({search_term} s{page}): {e}")
                    break

        return events