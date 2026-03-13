"""Agroforestry Sverige"""
import feedparser
from .base import BaseScraper


class AgroforestryScraper(BaseScraper):
    name = "Agroforestry Sverige"
    source_id = "AF"
    base_url = "https://agroforestry.se"
    EVENTS_URL = "https://agroforestry.se/evenemang/"
    RSS_URL = "https://agroforestry.se/feed/"

    def fetch(self) -> list[dict]:
        events = []

        # Prova RSS
        try:
            feed = feedparser.parse(self.RSS_URL)
            for entry in feed.entries:
                title = entry.get("title", "")
                desc = entry.get("summary", "")
                date_str = None
                if hasattr(entry, "published_parsed") and entry.published_parsed:
                    t = entry.published_parsed
                    date_str = f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d}"
                if not date_str:
                    continue
                events.append(self.event(
                    title=title,
                    date_iso=date_str,
                    url=entry.get("link", self.EVENTS_URL),
                    description=desc,
                    categories=["agroforestry", "mat", "skog"],
                ))
        except Exception as e:
            print(f"    AF RSS: {e}")

        # HTML-scraping av evenemangsida (WordPress Events Manager / The Events Calendar)
        if not events:
            try:
                soup = self.soup(self.EVENTS_URL)
                for item in soup.select(".event, article, .tribe-event"):
                    title_el = item.select_one("h2, h3, .tribe-event-name, a")
                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not title:
                        continue
                    date_el = item.select_one("time, .tribe-event-date-start, .date, abbr")
                    dt = ""
                    if date_el:
                        dt = date_el.get("datetime", date_el.get("title", date_el.get_text()))
                    date_str = self.parse_swedish_date(dt)
                    if not date_str:
                        continue
                    link_el = item.select_one("a[href]")
                    link = link_el["href"] if link_el else self.EVENTS_URL
                    events.append(self.event(
                        title=title, date_iso=date_str, url=link,
                        categories=["agroforestry"],
                    ))
            except Exception as e:
                print(f"    AF HTML: {e}")

        return events
