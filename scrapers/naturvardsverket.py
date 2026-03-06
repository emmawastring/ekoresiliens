"""Naturvårdsverket – hämtar eventdatum från kalendersidan."""
import feedparser
from .base import BaseScraper


class NaturvardsverketScraper(BaseScraper):
    name = "Naturvårdsverket"
    source_id = "NV"
    base_url = "https://www.naturvardsverket.se"
    CALENDAR_URL = "https://www.naturvardsverket.se/om-naturvardsverket/kalender/"
    RSS_URLS = [
        "https://www.naturvardsverket.se/rss/nyheter/",
        "https://www.naturvardsverket.se/rss/",
    ]

    def fetch(self) -> list[dict]:
        events = []

        # HTML-kalender – riktiga eventdatum
        try:
            soup = self.soup(self.CALENDAR_URL)
            for item in soup.select("article, li, .event, .calendar-item"):
                title_el = item.select_one("h2, h3, a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if not title or len(title) < 5:
                    continue

                time_el = item.select_one("time[datetime]")
                date_str = None
                if time_el:
                    date_str = self.parse_swedish_date(time_el["datetime"])
                if not date_str:
                    date_el = item.select_one("time, .date")
                    if date_el:
                        date_str = self.parse_swedish_date(date_el.get_text(strip=True))
                if not date_str:
                    continue

                link_el = item.select_one("a[href]")
                link = link_el["href"] if link_el else self.CALENDAR_URL
                if link and not link.startswith("http"):
                    link = self.base_url + link

                desc_el = item.select_one("p, .preamble")
                desc = desc_el.get_text(strip=True) if desc_el else ""

                events.append(self.event(
                    title=title, date_iso=date_str, url=link,
                    description=desc, categories=["klimat", "policy", "biodiv"],
                ))
        except Exception as e:
            print(f"    NV HTML: {e}")

        # RSS-fallback
        if not events:
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
                            url=entry.get("link", self.CALENDAR_URL),
                            description=desc,
                            categories=["klimat", "policy"],
                        ))
                except Exception as e:
                    print(f"    NV RSS {rss}: {e}")

        return events
