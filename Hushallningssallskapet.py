import requests
from .base import BaseScraper

SOURCE_ID   = "hushallningssallskapet"
SOURCE_NAME = "Hushållningssällskapet"
API_URL     = "https://hushallningssallskapet.se/wp-json/wp/v2/events"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

class HushallningssallskapetScraper(BaseScraper):
    source_id   = SOURCE_ID
    source_name = SOURCE_NAME

    def fetch(self):
        events = []
        page = 1
        while True:
            try:
                r = requests.get(
                    API_URL,
                    params={"per_page": 50, "page": page, "status": "publish"},
                    headers=HEADERS,
                    timeout=15
                )
                if r.status_code == 400:
                    break
                r.raise_for_status()
                items = r.json()
                if not items:
                    break
                for item in items:
                    try:
                        acf       = item.get("acf", {})
                        raw_date  = acf.get("event_date", "")
                        if not raw_date:
                            continue
                        # Format: YYYYMMDD → YYYY-MM-DD
                        date_iso  = f"{raw_date[:4]}-{raw_date[4:6]}-{raw_date[6:8]}"
                        title     = item["title"]["rendered"].strip()
                        url       = item.get("link", "")
                        from bs4 import BeautifulSoup
                        desc      = BeautifulSoup(
                            item.get("content", {}).get("rendered", ""), "html.parser"
                        ).get_text(" ", strip=True)[:300]
                        location  = ""
                        loc_link  = acf.get("event_location_link") or {}
                        if isinstance(loc_link, dict):
                            location = loc_link.get("title", "")
                        elif isinstance(loc_link, str):
                            location = loc_link
                        organizer = acf.get("event_organizer_name", "")
                        if organizer and location:
                            desc = f"{organizer} – {location}\n{desc}"
                        elif organizer:
                            desc = f"{organizer}\n{desc}"
                        events.append(self.event(
                            title=title,
                            date_iso=date_iso,
                            url=url,
                            description=desc,
                            categories=["samhalle"],
                        ))
                    except Exception as e:
                        print(f"  {SOURCE_NAME}: fel för item {item.get('id')}: {e}")
                page += 1
            except Exception as e:
                print(f"  {SOURCE_NAME}: fel sida {page}: {e}")
                break
        return events