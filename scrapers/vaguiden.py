"""VA-guiden – utbildningar och kurser"""
import requests, re, time
from bs4 import BeautifulSoup
from .base import BaseScraper

class VAGuidenScraper(BaseScraper):
    SOURCE_ID   = "vaguiden"
    source_id   = "vaguiden"
    SOURCE_NAME = "VA-guiden"
    name        = SOURCE_NAME
    BASE_URL    = "https://vaguiden.se"
    URL         = "https://vaguiden.se/utbildningar/"

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")

        events = []
        seen = set()

        for h3 in soup.find_all("h3"):
            title = h3.get_text(strip=True)
            if not title or len(title) < 5:
                continue

            parent = h3.find_parent(["article", "div", "li", "section"])
            a = parent.find("a", href=True) if parent else h3.find_parent("a")
            if not a:
                a = h3.find("a", href=True)
            if not a:
                continue

            url = a["href"]
            if url in seen:
                continue
            seen.add(url)

            if not url.startswith("http"):
                url = self.BASE_URL + url

            # Hämta datum från detaljsida
            date_iso_val = self._fetch_date(url, h)

            events.append(self.event(
                title=title,
                date_iso=date_iso_val or "",
                url=url,
                description="",
                categories=["vatten"],
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