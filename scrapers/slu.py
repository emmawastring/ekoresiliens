"""
SLU – Sveriges lantbruksuniversitet
Hämtar eventdatum från kalender-HTML, inte RSS-publiceringsdatum.
"""

import feedparser
from .base import BaseScraper


class SLUScraper(BaseScraper):
    name = "Sveriges lantbruksuniversitet (SLU)"
    source_id = "SLU"
    base_url = "https://www.slu.se"
    CALENDAR_URL = "https://www.slu.se/om-slu/kalender/"

    CATS_MAP = {
        "skog": ["skog"], "klimat": ["klimat"], "jordbruk": ["mat"],
        "livsmedel": ["mat"], "vatten": ["vatten"],
        "biodiversitet": ["biodiv"], "biologisk mångfald": ["biodiv"],
        "agroforestry": ["agroforestry"], "skogsträdgård": ["skogstradgard"],
    }

    def fetch(self) -> list[dict]:
        events = []

        # Försök 1: Hämta HTML-kalendern – SLU har strukturerade event-sidor
        try:
            soup = self.soup(self.CALENDAR_URL)
            # SLU använder article-element med time[datetime] för sina evenemang
            for item in soup.select("article, .event, .calendar-event, li.event"):
                title_el = item.select_one("h2, h3, .event-title, a")
                if not title_el:
                    continue
                title = title_el.get_text(strip=True)
                if not title or len(title) < 5:
                    continue

                # Hämta riktigt eventdatum från <time datetime="...">
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
                link = link_el["href"] if link_el else self.CALENDAR_URL
                if link and not link.startswith("http"):
                    link = self.base_url + link

                desc_el = item.select_one("p, .preamble, .description")
                desc = desc_el.get_text(strip=True) if desc_el else ""

                cats = self._guess_cats(title + " " + desc)
                events.append(self.event(
                    title=title, date_iso=date_str, url=link,
                    description=desc, categories=cats,
                ))
        except Exception as e:
            print(f"    SLU HTML: {e}")

        # Försök 2: RSS som fallback – publiceringsdatum men bättre än inget
        if not events:
            for feed_url in [
                "https://www.slu.se/rss/evenemang/",
                "https://www.slu.se/rss/kurser-och-utbildning/",
            ]:
                try:
                    feed = feedparser.parse(feed_url)
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
                        cats = self._guess_cats(title + " " + desc)
                        events.append(self.event(
                            title=title,
                            date_iso=date_str,
                            url=entry.get("link", self.CALENDAR_URL),
                            description=desc,
                            categories=cats,
                        ))
                except Exception as e:
                    print(f"    SLU RSS {feed_url}: {e}")

        return events

    def _guess_cats(self, text: str) -> list:
        text = text.lower()
        cats = set()
        for keyword, cats_list in self.CATS_MAP.items():
            if keyword in text:
                cats.update(cats_list)
        return list(cats) or ["biodiv"]
