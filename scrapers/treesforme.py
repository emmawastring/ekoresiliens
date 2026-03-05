"""Trees for Me"""
from .base import BaseScraper


class TreesForMeScraper(BaseScraper):
    name = "Trees for Me"
    source_id = "Trees for Me"
    base_url = "https://treesforme.se"
    EVENTS_URL = "https://treesforme.se/sv/kalendarium/"

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
                        categories=["biodiv", "skog", "mat"],
                    ))
        except Exception as e:
            print(f"    Trees for Me: {e}")
        return events