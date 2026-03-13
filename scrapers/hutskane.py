"""
Scraper for Hållbar Utveckling Skåne kalender
https://www.hutskane.se/kalender/
"""
import requests
from bs4 import BeautifulSoup
import re
from .base import BaseScraper


class HutSkaneScraper(BaseScraper):
    SOURCE_ID   = "hutskane"
    source_id = "hutskane"
    SOURCE_NAME = "Hållbar Utveckling Skåne"
    name = SOURCE_NAME
    BASE_URL    = "https://www.hutskane.se"
    CALENDAR_URL = "https://www.hutskane.se/kalender/lista/"

    MONTHS = {
        "januari": "01", "februari": "02", "mars": "03", "april": "04",
        "maj": "05", "juni": "06", "juli": "07", "augusti": "08",
        "september": "09", "oktober": "10", "november": "11", "december": "12"
    }

    def fetch(self):
        events = []
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Ekoresiliens/1.0)"}

        url = self.CALENDAR_URL
        while url:
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code != 200:
                    break
                soup = BeautifulSoup(r.text, "html.parser")

                # Hitta evenemang - varje li med datum och länk
                for article in soup.select("article.tribe-events-calendar-list__event"):
                    try:
                        # Titel
                        title_el = article.select_one(".tribe-events-calendar-list__event-title a, h3 a")
                        if not title_el:
                            continue
                        title = title_el.get_text(strip=True)
                        link  = title_el.get("href", "")

                        # Datum - från datetime-attributet
                        date_el = article.select_one("time[datetime]")
                        date_iso = None
                        if date_el and date_el.get("datetime"):
                            dt = date_el["datetime"]
                            date_iso = dt[:10]  # YYYY-MM-DD
                        else:
                            # Fallback: parsa texten t.ex. "10 mars 09:00"
                            date_text = article.get_text()
                            m = re.search(
                                r'(\d{1,2})\s+(januari|februari|mars|april|maj|juni|juli|augusti|september|oktober|november|december)\s*(\d{4})?',
                                date_text, re.IGNORECASE)
                            if m:
                                day   = m.group(1).zfill(2)
                                month = self.MONTHS.get(m.group(2).lower(), "01")
                                year  = m.group(3) or "2026"
                                date_iso = f"{year}-{month}-{day}"

                        if not date_iso:
                            continue

                        # Beskrivning
                        desc_el = article.select_one(".tribe-events-calendar-list__event-description, .tribe-event-description, p")
                        description = desc_el.get_text(strip=True)[:300] if desc_el else ""

                        # Plats
                        loc_el = article.select_one(".tribe-events-calendar-list__event-venue, .tribe-venue")
                        location = loc_el.get_text(strip=True) if loc_el else "Skåne"

                        events.append(self.event(
                            title=title,
                            date_iso=date_iso,
                            url=link or url,
                            description=description,
                            categories=["omstallning", "klimat"],
                            source_name=self.SOURCE_NAME,
                        ))

                    except Exception as e:
                        print(f"  HUT Skåne: fel på event: {e}")

                # Nästa sida?
                next_link = soup.select_one("a.tribe-events-nav-next, a[rel='next']")
                url = next_link["href"] if next_link else None

            except Exception as e:
                print(f"  HUT Skåne: fel: {e}")
                break

        return events