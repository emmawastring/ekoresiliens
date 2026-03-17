"""Landsbygdsnätverket – events scraper"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

class LandsbygdsnatverketScraper(BaseScraper):
    SOURCE_ID   = "landsbygdsnatverket"
    source_id   = "landsbygdsnatverket"
    SOURCE_NAME = "Landsbygdsnätverket"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.landsbygdsnatverket.se"
    URL         = "https://www.landsbygdsnatverket.se/kommandeaktiviteter.4.490b482015189b53667216b.html"

    MONTH_MAP = {
        'januari':1,'februari':2,'mars':3,'april':4,'maj':5,'juni':6,
        'juli':7,'augusti':8,'september':9,'oktober':10,'november':11,'december':12
    }

    def fetch(self, date_iso=None):
        h = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        events = []
        seen = set()

        for a in soup.find_all('a', href=True):
            href = a['href']
            if 'kalenderaktiviteter' not in href:
                continue
            title = a.get_text(strip=True)
            if not title or len(title) < 5 or href in seen:
                continue
            seen.add(href)

            url = href if href.startswith('http') else self.BASE_URL + href

            # Hämta detaljsida för datum
            date_iso_val = self._fetch_date(url, h)

            cats = self._guess_cats(title)
            events.append(self.event(
                title=title,
                date_iso=date_iso_val or '',
                url=url,
                description='',
                categories=cats,
            ))
        return events

    def _fetch_date(self, url, h):
        try:
            r = requests.get(url, headers=h, timeout=10)
            r.encoding = 'utf-8'
            text = r.text
            # ISO-datum
            m = re.search(r'(202[5-9]-\d{2}-\d{2})', text)
            if m:
                return m.group(1)
            # Svensk datum: "3 mars 2026"
            m2 = re.search(r'(\d{1,2})\s+(januari|februari|mars|april|maj|juni|juli|augusti|september|oktober|november|december)\s+(202[5-9])', text, re.I)
            if m2:
                day = int(m2.group(1))
                mon = self.MONTH_MAP.get(m2.group(2).lower())
                year = int(m2.group(3))
                if mon:
                    return f'{year}-{mon:02d}-{day:02d}'
        except:
            pass
        return None

    def _guess_cats(self, title):
        t = title.lower()
        if any(x in t for x in ['klimat', 'klimatanpassning', 'växtnäring', 'växthusgaser']): return ['klimat']
        if any(x in t for x in ['vatten', 'vattenbruk', 'fiske', 'sjömat', 'östersjö']): return ['vatten']
        if any(x in t for x in ['biologisk mångfald', 'betesmark', 'naturresturering']): return ['biodiv']
        if any(x in t for x in ['energi', 'biogas', 'förnybar']): return ['energi']
        if any(x in t for x in ['mat', 'livsmedel', 'ekologisk', 'odling']): return ['mat']
        if any(x in t for x in ['beredskap', 'krisberedskap', 'försvar']): return ['beredskap']
        if any(x in t for x in ['skog', 'skogbruk']): return ['skog']
        return ['omstallning']