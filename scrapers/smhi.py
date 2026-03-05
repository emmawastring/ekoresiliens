"""SMHI"""
import feedparser
from .base import BaseScraper


class SMHIScraper(BaseScraper):
    name = "SMHI"
    source_id = "SMHI"
    base_url = "https://www.smhi.se"
    EVENTS_URL = "https://www.smhi.se/om-smhi/aktuellt/"
    RSS_URL = "https://www.smhi.se/rss/nyheter.xml"

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
                    categories=["klimat"],
                ))
        except Exception as e:
            print(f"    SMHI: {e}")
        return events
