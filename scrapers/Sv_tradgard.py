"""SV – Studieförbundet Vuxenskolan, Trädgård"""
import requests, re
from bs4 import BeautifulSoup
from .base import BaseScraper

class SVTradgardScraper(BaseScraper):
    SOURCE_ID   = "sv_tradgard"
    source_id   = "sv_tradgard"
    SOURCE_NAME = "SV Studieförbundet"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.sv.se"
    URL         = "https://www.sv.se/kurser-och-evenemang/tradgard-hus-och-hem/tradgard"

    def fetch(self, date_iso=None):
        h = {'User-Agent': 'Mozilla/5.0'}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, 'html.parser')

        events = []
        seen = set()

        # Kurskort – leta efter artiklar/divs med datum och länk
        for card in soup.find_all(['article', 'div'], class_=re.compile(r'card|course|item|product', re.I)):
            a = card.find('a', href=True)
            if not a:
                continue
            href = a['href']
            if not href or href in seen:
                continue
            seen.add(href)

            title_el = card.find(['h2', 'h3', 'h4'])
            title = title_el.get_text(strip=True) if title_el else a.get_text(strip=True)
            if not title or len(title) < 5:
                continue

            # Datum – ISO-format i text
            text = card.get_text(' ', strip=True)
            date_iso_val = ''
            m = re.search(r'(202[5-9]-\d{2}-\d{2})', text)
            if m:
                date_iso_val = m.group(1)

            # Pris
            price_m = re.search(r'(\d[\d\s]+)\s*SEK', text)
            desc = f'{price_m.group(0)}' if price_m else ''

            url = href if href.startswith('http') else self.BASE_URL + href

            cats = ['omstallning']
            tl = title.lower()
            if any(x in tl for x in ['permakultur', 'skogsträdgård', 'skogsodling']): cats = ['skogstradgard']
            elif any(x in tl for x in ['skog', 'träd', 'frukt', 'bär']): cats = ['skog']
            elif any(x in tl for x in ['biologisk mångfald', 'pollinator', 'insekt']): cats = ['biodiv']
            elif any(x in tl for x in ['mat', 'grönsak', 'odl']): cats = ['mat']

            events.append(self.make_event(
                title=title,
                date_iso=date_iso_val,
                url=url,
                description=desc,
                categories=cats,
            ))
        return events