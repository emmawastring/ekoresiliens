"""
Länsstyrelsen – generisk scraper för alla länsstyrelsers kalendrar.
Länsstyrelsen använder konsekvent <time datetime="YYYY-MM-DD"> vilket ger riktiga eventdatum.
"""
from .base import BaseScraper


class LansstyrelseScraper(BaseScraper):
    def __init__(self, region: str, url: str):
        self.region = region
        self.name = f"Länsstyrelsen {region}"
        self.source_id = f"LS {region}"
        self.base_url = "https://www.lansstyrelsen.se"
        self.EVENTS_URL = url

    def fetch(self) -> list[dict]:
        events = []
        try:
            soup = self.soup(self.EVENTS_URL)

            # Länsstyrelsen använder article eller li med time[datetime]
            for item in soup.select("article, li, .event, .calendar-item"):
                title_el = item.select_one("h2, h3, a, .title")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if not title or len(title) < 5:
                    continue

                # Riktigt eventdatum från <time datetime="...">
                time_el = item.select_one("time[datetime]")
                date_str = None
                if time_el:
                    date_str = self.parse_swedish_date(time_el["datetime"])
                if not date_str:
                    date_el = item.select_one("time, .date, .event-date")
                    if date_el:
                        date_str = self.parse_swedish_date(date_el.get_text(strip=True))
                if not date_str:
                    continue

                link_el = item.select_one("a[href]")
                url = link_el["href"] if link_el else self.EVENTS_URL
                if url and not url.startswith("http"):
                    url = self.base_url + url

                desc_el = item.select_one("p, .preamble, .excerpt")
                desc = desc_el.get_text(strip=True) if desc_el else ""

                events.append(self.event(
                    title=title,
                    date_iso=date_str,
                    url=url,
                    description=desc,
                    categories=["omstallning", "klimat", "biodiv"],
                ))
        except Exception as e:
            print(f"    {self.name}: {e}")
        return events
