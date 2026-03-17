"""Nötverket – events och KB"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

class NotverketScraper(BaseScraper):
    SOURCE_ID   = "notverket"
    source_id   = "notverket"
    SOURCE_NAME = "Nötverket"
    name        = SOURCE_NAME
    BASE_URL    = "https://notverket.se"
    URL         = "https://notverket.se/events"

    MONTH_MAP = {
        'jan':1,'feb':2,'mar':3,'apr':4,'maj':5,'jun':6,
        'jul':7,'aug':8,'sep':9,'okt':10,'nov':11,'dec':12
    }

    def fetch(self, date_iso=None):
        h = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        events = []
        seen = set()

        for article in soup.find_all('article'):
            # Titel
            title_el = article.find(['h3', 'h2', 'h4'])
            title = title_el.get_text(strip=True) if title_el else ''
            if not title or title in seen:
                continue
            seen.add(title)

            # URL
            a = article.find('a', href=True)
            url = a['href'] if a else self.URL
            if url.startswith('/'):
                url = self.BASE_URL + url

            # Datum – ISO-format i texten
            text = article.get_text(' ', strip=True)
            m = re.search(r'(202[5-9]-\d{2}-\d{2})', text)
            date_iso_val = m.group(1) if m else ''

            events.append(self.event(
                title=title,
                date_iso=date_iso_val,
                url=url,
                description='',
                categories=['mat', 'skogstradgard'],
            ))
        return events