"""
Naturvårdsverket
Hämtar evenemang via RSS och HTML-scraping av evenemangsidan.
"""

import feedparser
from bs4 import BeautifulSoup
from .base import BaseScraper


class NaturvardsverketScraper(BaseScraper):
    name = "Naturvårdsverket"
    source_id = "NV"
    base_url = "https://www.naturvardsverket.se"

    EVENTS_URL = "https://www.naturvardsverket.se/om-naturvardsverket/evenemang/"
    RSS_URL = "https://www.naturvardsverket.se/rss/nyheter/"

    def fetch(self) -> list[dict]:
        events = []
        events.extend(self._from_rss())
        events.extend(self._from_html())
        return events

    def _from_rss(self) -> list:
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
                    categories=["klimat", "policy"],
                ))
        except Exception as e:
            print(f"    NV RSS: {e}")
        return events

    def _from_html(self) -> list:
        events = []
        try:
            soup = self.soup(self.EVENTS_URL)
            # Naturvårdsverket listar evenemang i article/li-element
            for item in soup.select("article, .event-item, li.event"):
                title_el = item.select_one("h2, h3, .title, a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if not title or not self.is_relevant(title):
                    continue

                link_el = item.select_one("a[href]")
                link = self.base_url + link_el["href"] if link_el and link_el["href"].startswith("/") else (link_el["href"] if link_el else self.EVENTS_URL)

                date_el = item.select_one("time, .date, [class*='date']")
                date_text = date_el.get_text(strip=True) if date_el else ""
                if date_el and date_el.get("datetime"):
                    date_text = date_el["datetime"]
                date_str = self.parse_swedish_date(date_text)
                if not date_str:
                    continue

                desc_el = item.select_one("p, .description, .preamble")
                desc = desc_el.get_text(strip=True) if desc_el else ""

                events.append(self.event(
                    title=title,
                    date_iso=date_str,
                    url=link,
                    description=desc,
                    categories=["klimat", "policy", "biodiv"],
                ))
        except Exception as e:
            print(f"    NV HTML: {e}")
        return events
