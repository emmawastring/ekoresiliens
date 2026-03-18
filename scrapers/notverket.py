"""Nötverket – events"""
import requests, re
from bs4 import BeautifulSoup
import time
from .base import BaseScraper

class NotverketScraper(BaseScraper):
    SOURCE_ID   = "notverket"
    source_id   = "notverket"
    SOURCE_NAME = "Nötverket"
    name        = SOURCE_NAME
    BASE_URL    = "https://notverket.se"
    URL         = "https://notverket.se/events"

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")

        events = []
        seen = set()

        for article in soup.find_all("article"):
            title_el = article.find(["h3", "h2", "h4"])
            title = title_el.get_text(strip=True) if title_el else ""
            if not title or title in seen:
                continue
            seen.add(title)

            a = article.find("a", href=True)
            url = a["href"] if a else self.URL
            if url.startswith("/"):
                url = self.BASE_URL + url

            # Hämta datum från detaljsida
            date_iso_val = self._fetch_date(url, h)

            events.append(self.event(
                title=title,
                date_iso=date_iso_val or "",
                url=url,
                description="",
                categories=["mat", "skogstradgard"],
            ))
            time.sleep(0.3)
        return events

    def _fetch_date(self, url, h):
        try:
            r = requests.get(url, headers=h, timeout=10)
            r.encoding = "utf-8"
            m = re.search(r"(202[5-9]-\d{2}-\d{2})", r.text)
            if m:
                return m.group(1)
        except:
            pass
        return None
