"""Permakultur Sverige"""
import feedparser
from .base import BaseScraper


class PermakulturScraper(BaseScraper):
    name = "Permakultur Sverige"
    source_id = "PF"
    base_url = "https://www.permakultur.se"
    EVENTS_URL = "https://www.permakultur.se/kurser/"
    RSS_URL = "https://www.permakultur.se/feed/"

    def fetch(self) -> list[dict]:
        events = []
        try:
            feed = feedparser.parse(self.RSS_URL)
            for entry in feed.entries:
                title = entry.get("title", "")
                desc = entry.get("summary", "")
                if not self.is_relevant(title, desc):
                    continue
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
                    categories=["skogstradgard", "mat", "biodiv"],
                ))
        except Exception as e:
            print(f"    PF: {e}")
        return events
