#!/usr/bin/env python3
"""
Ekoresiliens – webbinarieskrapare
Kör: python scraper.py
Skriver: ../data/webinars.json

Stöder tre strategier per källa:
  - rss   : feedparser läser RSS/Atom
  - ical  : icalendar läser .ics-flöden
  - html  : requests + BeautifulSoup scraper HTML-sidor
"""

import json
import re
import sys
import hashlib
import logging
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urljoin, urlparse

# Tredjepartsbibliotek (se requirements.txt)
try:
    import requests
    from bs4 import BeautifulSoup
    import feedparser
    from dateutil import parser as dateparser
except ImportError as e:
    print(f"Saknat bibliotek: {e}")
    print("Kör: pip install -r requirements.txt")
    sys.exit(1)

try:
    from icalendar import Calendar
    ICAL_AVAILABLE = True
except ImportError:
    ICAL_AVAILABLE = False

from sources import SOURCES, CATEGORY_KEYWORDS

# ── Konfiguration ──────────────────────────────────────────────
OUTPUT_FILE = Path(__file__).parent.parent / "data" / "webinars.json"
MAX_DAYS_AHEAD = 120       # Visa event upp till X dagar framåt
MAX_DAYS_PAST  = 1         # Inkludera event som slutade för max X dag(ar) sedan
REQUEST_TIMEOUT = 15       # sekunder
USER_AGENT = (
    "Mozilla/5.0 (compatible; Ekoresiliens-bot/1.0; "
    "+https://github.com/emmawastring/ekoresiliens)"
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("scraper")


# ── Hjälpfunktioner ────────────────────────────────────────────

def make_id(source_id: str, url: str, title: str) -> str:
    """Stabilt ID baserat på källa + URL/titel."""
    raw = f"{source_id}:{url or title}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


def get_session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT})
    return s


def safe_get(session: requests.Session, url: str):
    try:
        r = session.get(url, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        return r
    except Exception as e:
        log.warning(f"  Fel vid hämtning av {url}: {e}")
        return None


def parse_date(raw: str) -> datetime | None:
    """Försöker tolka datumsträngar av många format."""
    if not raw:
        return None
    raw = raw.strip()
    try:
        return dateparser.parse(raw, dayfirst=True)
    except Exception:
        pass
    # Försök extrahera datum med regex
    patterns = [
        r"(\d{4}-\d{2}-\d{2})",          # 2025-03-15
        r"(\d{1,2}/\d{1,2}/\d{4})",      # 15/3/2025
        r"(\d{1,2}\s+\w+\s+\d{4})",      # 15 mars 2025
    ]
    for pat in patterns:
        m = re.search(pat, raw)
        if m:
            try:
                return dateparser.parse(m.group(1), dayfirst=True)
            except Exception:
                pass
    return None


def is_in_window(dt: datetime | None) -> bool:
    """Returnerar True om datumet är inom det intressanta tidsfönstret."""
    if dt is None:
        return False
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    lower = now - timedelta(days=MAX_DAYS_PAST)
    upper = now + timedelta(days=MAX_DAYS_AHEAD)
    return lower <= dt <= upper


def guess_categories(text: str) -> list[str]:
    """Gissar kategorier baserat på nyckelord i text."""
    text_lower = text.lower()
    found = []
    for cat, keywords in CATEGORY_KEYWORDS.items():
        if any(kw in text_lower for kw in keywords):
            found.append(cat)
    return found or ["samhalle"]


def make_event(
    source: dict,
    title: str,
    description: str,
    date: datetime | None,
    url: str,
    extra_cats: list[str] | None = None,
) -> dict | None:
    """Normaliserar ett event till det gemensamma formatet."""
    title = title.strip() if title else ""
    description = (description or "").strip()

    if not title or len(title) < 5:
        return None
    if not is_in_window(date):
        return None

    all_text = f"{title} {description}"
    cats = list(set(guess_categories(all_text) + (extra_cats or source.get("categories", []))))
    cats = cats[:4]  # max 4 kategorier per event

    date_str = date.strftime("%Y-%m-%d") if date else None
    time_str = date.strftime("%H:%M") if date and date.hour != 0 else None

    return {
        "id":     make_id(source["id"], url, title),
        "source": source["name"],
        "title":  title,
        "desc":   description[:300] + ("…" if len(description) > 300 else ""),
        "date":   date_str,
        "time":   time_str,
        "url":    url or source["url"],
        "cats":   cats,
    }


# ── Scraper-strategier ──────────────────────────────────────────

def scrape_rss(source: dict, session: requests.Session) -> list[dict]:
    """Hämtar och tolkar RSS/Atom-flöde."""
    log.info(f"  RSS: {source['url']}")
    events = []
    try:
        feed = feedparser.parse(source["url"])
        for entry in feed.entries:
            title = entry.get("title", "")
            desc  = BeautifulSoup(
                entry.get("summary", entry.get("description", "")), "html.parser"
            ).get_text(separator=" ")

            # Datum – försök flera fält
            raw_date = (
                entry.get("published")
                or entry.get("updated")
                or entry.get("dc_date")
                or ""
            )
            dt = parse_date(raw_date)
            url = entry.get("link", source["url"])

            ev = make_event(source, title, desc, dt, url)
            if ev:
                events.append(ev)
    except Exception as e:
        log.warning(f"  RSS-fel för {source['id']}: {e}")
    log.info(f"  → {len(events)} event")
    return events


def scrape_ical(source: dict, session: requests.Session) -> list[dict]:
    """Hämtar och tolkar iCal-flöde."""
    if not ICAL_AVAILABLE:
        log.warning("  icalendar ej installerat, hoppar över iCal-källa")
        return []
    log.info(f"  iCal: {source['url']}")
    events = []
    r = safe_get(session, source["url"])
    if not r:
        return []
    try:
        cal = Calendar.from_ical(r.content)
        for component in cal.walk():
            if component.name != "VEVENT":
                continue
            title = str(component.get("SUMMARY", ""))
            desc  = str(component.get("DESCRIPTION", ""))
            dtstart = component.get("DTSTART")
            url   = str(component.get("URL", source["url"]))
            dt = None
            if dtstart:
                raw = dtstart.dt
                if hasattr(raw, "hour"):
                    dt = raw if raw.tzinfo else raw.replace(tzinfo=timezone.utc)
                else:
                    dt = datetime(raw.year, raw.month, raw.day, tzinfo=timezone.utc)
            ev = make_event(source, title, desc, dt, url)
            if ev:
                events.append(ev)
    except Exception as e:
        log.warning(f"  iCal-fel för {source['id']}: {e}")
    log.info(f"  → {len(events)} event")
    return events


def scrape_html(source: dict, session: requests.Session) -> list[dict]:
    """Scraper HTML-sida med BeautifulSoup."""
    log.info(f"  HTML: {source['url']}")
    cfg = source.get("scraper_config", {})
    events = []
    r = safe_get(session, source["url"])
    if not r:
        return []

    soup = BeautifulSoup(r.text, "html.parser")
    base_url = f"{urlparse(source['url']).scheme}://{urlparse(source['url']).netloc}"

    # Försök flera selektorer för event-container
    event_selectors = cfg.get("event_selector", "article, li.event, .event").split(", ")
    containers = []
    for sel in event_selectors:
        sel = sel.strip()
        found = soup.select(sel)
        if found:
            containers = found
            break

    # Fallback: alla article-taggar
    if not containers:
        containers = soup.find_all("article") or soup.find_all("li")

    log.info(f"    Hittade {len(containers)} containers")

    for container in containers[:30]:  # max 30 per sida
        # Titel
        title = ""
        for sel in cfg.get("title_selector", "h2, h3, a").split(", "):
            el = container.select_one(sel.strip())
            if el and el.get_text(strip=True):
                title = el.get_text(strip=True)
                break

        # Beskrivning
        desc = ""
        for sel in cfg.get("description_selector", "p").split(", "):
            el = container.select_one(sel.strip())
            if el and el.get_text(strip=True):
                desc = el.get_text(strip=True)
                break

        # Datum – försök <time datetime=...> först
        dt = None
        time_el = container.find("time")
        if time_el:
            dt = parse_date(time_el.get("datetime") or time_el.get_text(strip=True))
        if not dt:
            for sel in cfg.get("date_selector", ".date").split(", "):
                el = container.select_one(sel.strip())
                if el:
                    dt = parse_date(el.get("datetime") or el.get_text(strip=True))
                    if dt:
                        break

        # URL
        link_el = container.select_one("a[href]")
        href = link_el["href"] if link_el else ""
        if href and not href.startswith("http"):
            href = urljoin(base_url, href)

        ev = make_event(source, title, desc, dt, href or source["url"])
        if ev:
            events.append(ev)

    log.info(f"  → {len(events)} event")
    return events


# ── Huvud ──────────────────────────────────────────────────────

def run_all_scrapers() -> list[dict]:
    session = get_session()
    all_events = []

    for source in SOURCES:
        log.info(f"Hämtar {source['full_name']} ({source['strategy']})")
        strategy = source["strategy"]
        try:
            if strategy == "rss":
                events = scrape_rss(source, session)
            elif strategy == "ical":
                events = scrape_ical(source, session)
            elif strategy == "html":
                events = scrape_html(source, session)
            else:
                log.warning(f"  Okänd strategi: {strategy}")
                events = []
        except Exception as e:
            log.error(f"  Oväntat fel för {source['id']}: {e}")
            events = []

        all_events.extend(events)

    return all_events


def deduplicate(events: list[dict]) -> list[dict]:
    """Tar bort dubbletter baserat på ID."""
    seen = set()
    unique = []
    for ev in events:
        if ev["id"] not in seen:
            seen.add(ev["id"])
            unique.append(ev)
    return unique


def sort_events(events: list[dict]) -> list[dict]:
    """Sorterar på datum, event utan datum hamnar sist."""
    def sort_key(e):
        return e.get("date") or "9999-99-99"
    return sorted(events, key=sort_key)


def save_json(events: list[dict]):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    output = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "count": len(events),
        "events": events,
    }
    OUTPUT_FILE.write_text(json.dumps(output, ensure_ascii=False, indent=2))
    log.info(f"Sparade {len(events)} event till {OUTPUT_FILE}")


if __name__ == "__main__":
    log.info("=== Ekoresiliens scraper startar ===")
    events = run_all_scrapers()
    events = deduplicate(events)
    events = sort_events(events)
    log.info(f"Totalt: {len(events)} unika event inom tidsfönstret")
    save_json(events)
    log.info("=== Klar ===")
