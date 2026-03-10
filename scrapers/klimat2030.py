"""Klimat 2030"""
from .base import BaseScraper


class Klimat2030Scraper(BaseScraper):
    name = "Klimat 2030"
    source_id = "Klimat 2030"
    base_url = "https://klimat2030.se"
    EVENTS_URL = "https://klimat2030.se/category/evenemang/"

    def fetch(self) -> list[dict]:
        events = []
        try:
            soup = self.soup(self.EVENTS_URL)
            event_elements = soup.select("article, .event, li")

            for element in event_elements:
                title_elem = element.select_one("h2, h3, a")
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                if not self.is_relevant(title):
                    continue

                date_elem = element.select_one("time, .date")
                date_str = None
                if date_elem:
                    date_str = self.parse_swedish_date(date_elem.get_text(strip=True))

                desc_elem = element.select_one("p, .excerpt")
                description = desc_elem.get_text(strip=True) if desc_elem else ""

                link_elem = element.select_one("a")
                url = link_elem.get("href") if link_elem else self.EVENTS_URL
                if url and not url.startswith("http"):
                    url = self.base_url + url

                if date_str:
                    events.append(self.event(
                        title=title,
                        date_iso=date_str,
                        url=url,
                        description=description,
                        categories=["klimat", "omstallning", "policy"],
                    ))
        except Exception as e:
            print(f"    Klimat 2030: {e}")
        return events