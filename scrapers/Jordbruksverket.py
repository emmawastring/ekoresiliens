"""Jordbruksverket – kurser och seminarier"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

class JordbruksverketScraper(BaseScraper):
    SOURCE_ID   = "jordbruksverket"
    source_id   = "jordbruksverket"
    SOURCE_NAME = "Jordbruksverket"
    name        = SOURCE_NAME
    BASE_URL    = "https://jordbruksverket.se"
    URL         = "https://jordbruksverket.se/om-jordbruksverket/kurser-och-seminarier"

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
        # Tabell med kurser
        table = soup.find('table')
        if not table:
            return events

        rows = table.find_all('tr')
        for row in rows[1:]:  # hoppa header
            cells = row.find_all('td')
            if len(cells) < 4:
                continue
            date_text = cells[0].get_text(strip=True)
            title     = cells[1].get_text(strip=True)
            place     = cells[2].get_text(strip=True)
            link_el   = cells[3].find('a')
            url       = (link_el['href'] if link_el else None)
            if url and url.startswith('/'):
                url = self.BASE_URL + url

            date_iso_val = self._parse_date(date_text)
            if not date_iso_val:
                continue

            cats = ['omstallning']
            tl = (title + ' ' + (place or '')).lower()
            if any(x in tl for x in ['klimat', 'koldioxid', 'växthus']): cats = ['klimat']
            if any(x in tl for x in ['skog', 'träd']): cats = ['skog']
            if any(x in tl for x in ['vatten', 'bevattning']): cats = ['vatten']
            if any(x in tl for x in ['energi', 'biogas']): cats = ['energi']
            if any(x in tl for x in ['mat', 'livsmedel', 'kött', 'mjölk', 'spannmål']): cats = ['mat']
            if any(x in tl for x in ['bidrag', 'stöd', 'lag', 'regler']): cats = ['policy']

            events.append(self.event(
                title=title,
                date_iso=date_iso_val,
                url=url or self.URL,
                description=f'Plats: {place}' if place else '',
                categories=cats,
            ))
        return events

    def _parse_date(self, text):
        # "12 mars" eller "12-13 mars" eller ISO "2026-03-12"
        if re.match(r'^\d{4}-\d{2}-\d{2}$', text):
            return text
        import datetime
        m = re.search(r'(\d{1,2})\s+(\w+)', text.lower())
        if m:
            day = int(m.group(1))
            mon_str = m.group(2)[:3]
            mon = self.MONTH_MAP.get(mon_str)
            if mon:
                year = datetime.date.today().year
                if mon < datetime.date.today().month - 1:
                    year += 1
                return f'{year}-{mon:02d}-{day:02d}'
        return None