"""LU Land – Lunds universitets centrum för landskapsforskning"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

MONTH_MAP = {
    'jan':1,'feb':2,'mar':3,'apr':4,'maj':5,'jun':6,
    'jul':7,'aug':8,'sep':9,'okt':10,'nov':11,'dec':12,
    'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,
    'july':7,'august':8,'september':9,'october':10,'november':11,'december':12
}

def parse_sv_date(text):
    import datetime
    m = re.search(r'(\d{1,2})\s+(\w+)\s+(202[5-9])', text, re.I)
    if m:
        day = int(m.group(1))
        mon = MONTH_MAP.get(m.group(2).lower()[:3])
        year = int(m.group(3))
        if mon:
            return f'{year}-{mon:02d}-{day:02d}'
    return ''

class LULandScraper(BaseScraper):
    SOURCE_ID   = "luland"
    source_id   = "luland"
    SOURCE_NAME = "LU Land"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.luland.lu.se"
    URL         = "https://www.luland.lu.se/calendar"

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        events = []
        seen = set()
        for h3 in soup.find_all("h3"):
            title = h3.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            parent = h3.find_parent(["article","div","li","section"])
            a = parent.find("a", href=True) if parent else None
            if not a:
                continue
            href = a["href"]
            if href in seen:
                continue
            seen.add(href)
            url = href if href.startswith("http") else self.BASE_URL + href
            txt = parent.get_text(' ', strip=True) if parent else ''
            date = parse_sv_date(txt)
            events.append(self.event(
                title=title, date_iso=date, url=url,
                description="", categories=["klimat","omstallning"],
            ))
        return events


class LUCSUSScraper(BaseScraper):
    SOURCE_ID   = "lucsus"
    source_id   = "lucsus"
    SOURCE_NAME = "LUCSUS"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.lucsus.lu.se"
    URL         = "https://www.lucsus.lu.se/calendar"

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = "utf-8"
        soup = BeautifulSoup(r.text, "html.parser")
        events = []
        seen = set()
        for h3 in soup.find_all("h3"):
            title = h3.get_text(strip=True)
            if not title or len(title) < 5:
                continue
            parent = h3.find_parent(["article","div","li","section"])
            a = parent.find("a", href=True) if parent else None
            if not a:
                continue
            href = a["href"]
            if href in seen:
                continue
            seen.add(href)
            url = href if href.startswith("http") else self.BASE_URL + href
            txt = parent.get_text(' ', strip=True) if parent else ''
            date = parse_sv_date(txt)
            events.append(self.event(
                title=title, date_iso=date, url=url,
                description="", categories=["omstallning","klimat"],
            ))
        return events


class LUHallbarhetScraper(BaseScraper):
    SOURCE_ID   = "lu_hallbarhet"
    source_id   = "lu_hallbarhet"
    SOURCE_NAME = "Lunds universitet"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.lu.se"
    URLS = [
        "https://www.lu.se/calendar?category=7958",
        "https://www.lu.se/calendar?category=7679",
    ]

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        events = []
        seen = set()
        for url in self.URLS:
            r = requests.get(url, headers=h, timeout=15)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")
            for h3 in soup.find_all("h3"):
                title = h3.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                parent = h3.find_parent(["article","div","li","section"])
                a = parent.find("a", href=True) if parent else None
                if not a:
                    continue
                href = a["href"]
                if href in seen:
                    continue
                seen.add(href)
                full_url = href if href.startswith("http") else self.BASE_URL + href
                txt = parent.get_text(' ', strip=True) if parent else ''
                date = parse_sv_date(txt)
                events.append(self.event(
                    title=title, date_iso=date, url=full_url,
                    description="", categories=["klimat","omstallning"],
                ))
        return events