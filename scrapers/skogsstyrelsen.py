"""
Skogsstyrelsen
"""

import feedparser
from .base import BaseScraper


class SkogsstyrelseScraper(BaseScraper):
    name = "Skogsstyrelsen"
    source_id = "SKS"
    base_url = "https://www.skogsstyrelsen.se"

    EVENTS_URL = "https://www.skogsstyrelsen.se/kalender/"
    RSS_URLS = [
        "https://www.skogsstyrelsen.se/rss/nyheter/",
        "https://www.skogsstyrelsen.se/rss/evenemang/",
    ]

    def fetch(self) -> list[dict]:
        events = []
        for rss in self.RSS_URLS:
            try:
                feed = feedparser.parse(rss)
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
                        categories=["skog", "biodiv"],
                    ))
            except Exception as e:
                print(f"    SKS {rss}: {e}")

        # HTML-fallback
        if not events:
            try:
                soup = self.soup(self.EVENTS_URL)
                for item in soup.select("article, .event, li"):
                    title_el = item.select_one("h2, h3, a")
                    if not title_el:
                        continue
                    title = title_el.get_text(strip=True)
                    if not title or not self.is_relevant(title):
                        continue
                    date_el = item.select_one("time, .date")
                    dt = date_el.get("datetime", date_el.get_text()) if date_el else ""
                    date_str = self.parse_swedish_date(dt)
                    if not date_str:
                        continue
                    link_el = item.select_one("a[href]")
                    link = (self.base_url + link_el["href"] if link_el and link_el["href"].startswith("/")
                            else (link_el["href"] if link_el else self.EVENTS_URL))
                    events.append(self.event(
                        title=title, date_iso=date_str, url=link,
                        categories=["skog"],
                    ))
            except Exception as e:
                print(f"    SKS HTML: {e}")

        return events
