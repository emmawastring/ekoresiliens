"""Svensk Kolinlagring – kalendarium"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

class SvenskKolinlagringScraper(BaseScraper):
    SOURCE_ID   = "svenskkolinlagring"
    source_id   = "svenskkolinlagring"
    SOURCE_NAME = "Svensk Kolinlagring"
    name        = SOURCE_NAME
    BASE_URL    = "https://svenskkolinlagring.se"
    URL         = "https://svenskkolinlagring.se/kalendarium/"

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
        # Event-kort länkade till /kalenderpost/
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/kalenderpost/' not in href:
                continue
            title = a.get_text(' ', strip=True)
            if not title or len(title) < 5:
                # Kolla parent
                parent = a.find_parent(['article', 'div', 'section'])
                if parent:
                    title = parent.get_text(' ', strip=True)[:100]

            # Datum – leta i närheten
            container = a.find_parent(['article', 'div']) or a
            # Sök syskon/förälder text för datum
            text = ''
            for p in [container] + list(container.parents)[:3]:
                text = p.get_text(' ', strip=True)
                if re.search(r'\d{1,2}\s+\w+\s+202[5-9]', text):
                    break

            date_iso_val = self._parse_sv_date(text)

            url = href if href.startswith('http') else self.BASE_URL + href

            if not title or title in [e['title'] for e in events]:
                continue

            events.append(self.make_event(
                title=title[:120],
                date_iso=date_iso_val or '',
                url=url,
                description='',
                categories=['omstallning', 'mat'],
            ))
        return events

    def _parse_sv_date(self, text):
        import datetime
        m = re.search(r'(\d{1,2})\s+(jan|feb|mar|apr|maj|jun|jul|aug|sep|okt|nov|dec)\w*\s+(202[5-9])', text, re.I)
        if m:
            day = int(m.group(1))
            mon = self.MONTH_MAP.get(m.group(2).lower()[:3])
            year = int(m.group(3))
            if mon:
                return f'{year}-{mon:02d}-{day:02d}'
        return None