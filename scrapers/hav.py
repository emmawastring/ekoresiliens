"""Havs- och vattenmyndigheten – kalender"""
import requests
import re
from datetime import datetime
from bs4 import BeautifulSoup
from .base import BaseScraper

SOURCE_NAME = "Havs- och vattenmyndigheten"
BASE_URL    = "https://www.havochvatten.se"
CAL_URL     = f"{BASE_URL}/om-oss-kontakt-och-karriar/evenemang/kalender.html"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

MONTHS = {
    "jan":1,"feb":2,"mar":3,"apr":4,"maj":5,"jun":6,
    "jul":7,"aug":8,"sep":9,"okt":10,"nov":11,"dec":12
}

def parse_title_date(title):
    m = re.match(r'^(\d{1,2})\s+([a-z]{3})\s+(.+)$', title.strip().lower())
    if m:
        day   = int(m.group(1))
        month = MONTHS.get(m.group(2))
        year  = datetime.now().year
        now   = datetime.now()
        if month and month < now.month:
            year += 1
        parts = title.strip().split(' ', 2)
        clean = parts[2] if len(parts) > 2 else title
        if month:
            return f"{year}-{month:02d}-{day:02d}", clean
    return None, title

class HaVScraper(BaseScraper):
    name      = SOURCE_NAME
    source_id = "hav"

    def fetch(self) -> list[dict]:
        events = []
        seen = set()
        try:
            r = requests.get(CAL_URL, headers=HEADERS, timeout=15)
            r.encoding = "utf-8"
            r.raise_for_status()
            soup = BeautifulSoup(r.text, "html.parser")

            for a in soup.select("a.hav-list__items--item-link"):
                href      = a.get("href", "")
                title_raw = a.get("title", "") or a.get_text(strip=True)
                if not title_raw:
                    continue

                url = href if href.startswith("http") else BASE_URL + href
                if url in seen:
                    continue
                seen.add(url)

                # Datum i href
                m = re.search(r'/(\d{4}-\d{2}-\d{2})-', href)
                if m:
                    date_iso    = m.group(1)
                    clean_title = re.sub(r'^\d{1,2}\s+\w+\s+', '', title_raw).strip()
                else:
                    date_iso, clean_title = parse_title_date(title_raw)

                if not date_iso:
                    continue

                events.append(self.event(
                    title=clean_title or title_raw,
                    date_iso=date_iso,
                    url=url,
                    description="",
                    categories=["vatten", "biodiv", "klimat"],
                ))

        except Exception as e:
            print(f"  {SOURCE_NAME}: fel: {e}")

        return events