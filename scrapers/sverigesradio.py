"""Vetenskap & Allmänhet"""
import feedparser
from .base import BaseScraper


class SVAScraper(BaseScraper):
    name = "Vetenskap & Allmänhet"
    source_id = "SVA"
    base_url = "https://v-a.se"
    EVENTS_URL = "https://v-a.se/aktiviteter/"
    RSS_URL = "https://v-a.se/feed/"

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
                    categories=["samhalle"],
                ))
        except Exception as e:
            print(f"    SVA: {e}")
        return events
