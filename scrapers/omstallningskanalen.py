"""
Scraper for Omställningskanalen programserier
https://omstallningskanalen.se/programserier
API: https://omstallningskanalen.se/api/series
"""
import requests
from .base import BaseScraper


class OmstallningskanalenScraper(BaseScraper):
    SOURCE_ID   = "omstallningskanalen"
    SOURCE_NAME = "Omställningskanalen"
    API_URL     = "https://omstallningskanalen.se/api/series"
    BASE_URL    = "https://omstallningskanalen.se/programserier"

    def fetch(self):
        events = []
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; Ekoresiliens/1.0)",
            "Accept": "application/json",
        }

        try:
            r = requests.get(self.API_URL, headers=headers, timeout=15)
            r.raise_for_status()
            series = r.json()

            for item in series:
                if item.get("videoCount", 0) == 0:
                    continue  # Hoppa över tomma serier

                title       = item.get("title", "")
                description = item.get("description", "")[:300]
                created_at  = item.get("createdAt", "")[:10]  # YYYY-MM-DD

                events.append(self.event(
                    title=title,
                    date=created_at or "2026-01-01",
                    url=self.BASE_URL,
                    description=description,
                    categories=["samhalle", "klimat"],
                    source_name=self.SOURCE_NAME,
                ))

        except Exception as e:
            print(f"  Omställningskanalen: fel: {e}")

        return events