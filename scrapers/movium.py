"""SLU MOVIUM"""
from .base import BaseScraper


class MoviumScraper(BaseScraper):
    name = "SLU MOVIUM"
    source_id = "MOVIUM"
    base_url = "https://movium.slu.se"
    EVENTS_URL = "https://movium.slu.se/kalendarium/"

    def fetch(self) -> list[dict]:
        events = []
        try:
            soup = self.soup(self.EVENTS_URL)
            event_elements = soup.select("article, .event, .post, li")

            for element in event_elements:
                title_elem = element.select_one("h2, h3, a")
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                if not self.is_relevant(title):
                    continue

                date_elem = element.select_one("time, .date, .published")
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
                        categories=["samhalle", "biodiv", "skog"],
                    ))
        except Exception as e:
            print(f"    MOVIUM: {e}")
        return events