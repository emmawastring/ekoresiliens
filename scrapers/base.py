"""
Basklass för alla scrapers.
Varje scraper ärver från BaseScraper och implementerar fetch().
"""

import re
import hashlib
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup


class BaseScraper(ABC):
    name: str = "BaseScraper"
    source_id: str = "unknown"
    base_url: str = ""

    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (compatible; Ekoresiliens/1.0; "
            "+https://github.com/emmawastring/ekoresiliens)"
        )
    }
    TIMEOUT = 15

    # Nyckelord för att filtrera bort IRRELEVANTA evenemang (blacklist istället för whitelist)
    IRRELEVANT_KEYWORDS = [
        "shopping", "försäljning", "promotion", "discount", "köp",
        "sport", "dans", "teater", "musik", "biljetter",
        "konsert", "match", "äventyr", "tour", "resa",
    ]

    def is_relevant(self, title: str, description: str = "") -> bool:
        """
        Returnerar True om eventet INTE är uppenbart irrelevant.
        Använder blacklist istället för whitelist för att få mer data.
        """
        text = (title + " " + description).lower()
        # Filtrera bara bort uppenbart irrelevant innehål
        return not any(kw in text for kw in self.IRRELEVANT_KEYWORDS)

    def get(self, url: str, **kwargs) -> requests.Response:
        return requests.get(url, headers=self.HEADERS, timeout=self.TIMEOUT, **kwargs)

    def soup(self, url: str, **kwargs) -> BeautifulSoup:
        r = self.get(url, **kwargs)
        r.raise_for_status()
        return BeautifulSoup(r.text, "html.parser")

    def make_id(self, title: str, date: str) -> str:
        return hashlib.md5(f"{self.source_id}:{title}:{date}".encode()).hexdigest()[:12]

    def event(
        self,
        title: str,
        date_iso: str,           # "2025-06-15"
        url: str,
        description: str = "",
        time: str = "",          # "13:00–14:30"
        categories: Optional[list] = None,
        source_name: Optional[str] = None,
    ) -> dict:
        return {
            "id": self.make_id(title, date_iso),
            "title": title.strip(),
            "date_iso": date_iso,
            "time": time,
            "description": description.strip()[:400],
            "url": url,
            "source_id": self.source_id,
            "source_name": source_name or self.name,
            "categories": categories or [],
            "free": True,
        }

    def parse_swedish_date(self, text: str) -> Optional[str]:
        """
        Försöker parsa vanliga svenska datumformat till ISO-format.
        Returnerar "YYYY-MM-DD" eller None.
        """
        text = text.strip().lower()
        months = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "maj": 5, "jun": 6,
            "jul": 7, "aug": 8, "sep": 9, "okt": 10, "nov": 11, "dec": 12,
            "januari": 1, "februari": 2, "mars": 3, "april": 4, "juni": 6,
            "juli": 7, "augusti": 8, "september": 9, "oktober": 10,
            "november": 11, "december": 12,
        }
        year = datetime.now().year

        # "15 juni 2025" eller "15 juni"
        m = re.search(r"(\d{1,2})\s+(\w+)\s*(\d{4})?", text)
        if m:
            day = int(m.group(1))
            mon_str = m.group(2)[:3]
            yr = int(m.group(3)) if m.group(3) else year
            month = months.get(mon_str)
            if month:
                try:
                    return datetime(yr, month, day).strftime("%Y-%m-%d")
                except ValueError:
                    pass

        # "2025-06-15" eller "2025/06/15"
        m = re.search(r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})", text)
        if m:
            return f"{m.group(1)}-{int(m.group(2)):02d}-{int(m.group(3)):02d}"

        return None

    def generic_fetch(self) -> list[dict]:
        """
        En enkel fallback som skannar efter länkar och försöker extrahera datum
        från länktext eller närliggande text. Används av run_all om normal fetch
        inte hittar något.
        """
        events: list[dict] = []
        try:
            soup = self.soup(getattr(self, 'EVENTS_URL', self.base_url))
            for link in soup.find_all('a', href=True):
                title = link.get_text(' ', strip=True)
                if not title:
                    continue
                date_iso = self.parse_swedish_date(title)
                if not date_iso:
                    # kolla hos grannar
                    nearby = []
                    for sib in list(link.previous_siblings)[:3] + list(link.next_siblings)[:3]:
                        if hasattr(sib, 'get_text'):
                            nearby.append(sib.get_text(' ', strip=True))
                    date_iso = self.parse_swedish_date(' '.join(nearby))
                if date_iso and self.is_relevant(title):
                    url = link['href']
                    if url and not url.startswith('http'):
                        url = self.base_url.rstrip('/') + '/' + url.lstrip('/')
                    events.append(self.event(title=title, date_iso=date_iso, url=url))
        except Exception as e:
            print(f"{self.name} generic_fetch error: {e}")
        return events

    @abstractmethod
    def fetch(self) -> list[dict]:
        """Hämta och returnera lista av event-dicts."""
        ...
