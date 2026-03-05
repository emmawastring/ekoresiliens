"""
SLU – Sveriges lantbruksuniversitet
Hämtar evenemang via RSS-feed och kalender-sida.
"""

import feedparser
from .base import BaseScraper


class SLUScraper(BaseScraper):
    name = "Sveriges lantbruksuniversitet (SLU)"
    source_id = "SLU"
    base_url = "https://www.slu.se"

    FEEDS = [
        "https://www.slu.se/rss/evenemang/",
        "https://www.slu.se/rss/kurser-och-utbildning/",
    ]

    CATS_MAP = {
        "skog": ["skog"],
        "klimat": ["klimat"],
        "jordbruk": ["mat"],
        "livsmedel": ["mat"],
        "vatten": ["vatten"],
        "biodiversitet": ["biodiv"],
        "biologisk mångfald": ["biodiv"],
        "agroforestry": ["agroforestry"],
        "skogsträdgård": ["skogstradgard"],
    }

    def fetch(self) -> list[dict]:
        events = []
        for feed_url in self.FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                for entry in feed.entries:
                    title = entry.get("title", "")
                    desc = entry.get("summary", "")
                    link = entry.get("link", "")

                    if not self.is_relevant(title, desc):
                        continue

                    # Datum från published eller updated
                    date_str = None
                    if hasattr(entry, "published_parsed") and entry.published_parsed:
                        import time
                        t = entry.published_parsed
                        date_str = f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d}"
                    elif hasattr(entry, "updated_parsed") and entry.updated_parsed:
                        t = entry.updated_parsed
                        date_str = f"{t.tm_year}-{t.tm_mon:02d}-{t.tm_mday:02d}"

                    if not date_str:
                        continue

                    cats = self._guess_cats(title + " " + desc)
                    events.append(self.event(
                        title=title,
                        date_iso=date_str,
                        url=link or self.base_url + "/om-slu/kalender/",
                        description=desc,
                        categories=cats,
                    ))
            except Exception as e:
                print(f"    SLU feed {feed_url}: {e}")

        return events

    def _guess_cats(self, text: str) -> list:
        text = text.lower()
        cats = set()
        for keyword, cats_list in self.CATS_MAP.items():
            if keyword in text:
                cats.update(cats_list)
        return list(cats) or ["biodiv"]
