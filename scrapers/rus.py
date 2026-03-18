"""RUS – Regional Utveckling och Samverkan i miljömålssystemet"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

class RUSScraper(BaseScraper):
    SOURCE_ID   = "rus"
    source_id   = "rus"
    SOURCE_NAME = "RUS Miljömål"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.rus.se"
    URL         = "https://www.rus.se/"

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")

        events = []
        seen = set()

        for article in soup.find_all("article"):
            a = article.find("a", href=True)
            if not a:
                continue
            url = a["href"]
            if url in seen:
                continue
            seen.add(url)

            title_el = article.find(["h2", "h3", "h4"])
            title = title_el.get_text(strip=True) if title_el else a.get_text(strip=True)
            if not title or len(title) < 5:
                continue

            dates = re.findall(r"(202[0-9]-\d{2}-\d{2})", str(article))
            date_iso_val = dates[0] if dates else ""

            if not url.startswith("http"):
                url = self.BASE_URL + url

            events.append(self.event(
                title=title,
                date_iso=date_iso_val,
                url=url,
                description="",
                categories=["klimat", "omstallning"],
            ))
        return events