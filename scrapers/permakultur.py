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
                # Försök extrahera eventdatum från titel/beskrivning
                date_str = self.parse_swedish_date(title + " " + desc)
                if not date_str:
                    # Om vi inte kan parsa eventdatum, hoppa över
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
