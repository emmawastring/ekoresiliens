import re

from .base import BaseScraper

class EkocentrumScraper(BaseScraper):
    name = "Ekocentrum"
    source_id = "ekocentrum"
    base_url = "https://www.ekocentrum.se"
    EVENTS_URL = "https://www.ekocentrum.se/kalendarium-start/"
    
    def fetch(self) -> list[dict]:
        events = []
        try:
            soup = self.soup(self.EVENTS_URL)

            for h3 in soup.select('h3'):
                link = h3.select_one('a')
                if not link:
                    continue

                title = link.get_text(strip=True)
                href = link.get('href', '')
                if not title or not href:
                    continue
                if not href.startswith('http'):
                    href = self.base_url.rstrip('/') + '/' + href.lstrip('/')

                # hämta datum från länkens detaljsida eftersom indexsidan inte innehåller datum
                date_iso = None
                try:
                    detail = self.soup(href)
                    # leta efter text "Datum:" följt av datum
                    text = detail.get_text(' ', strip=True)
                    m = re.search(r"Datum[:\s]*(\d{1,2}\s+\w+\s+\d{4})", text)
                    if m:
                        date_iso = self.parse_swedish_date(m.group(1))
                    else:
                        # som fallback, försök hitta <time> element
                        t = detail.select_one('time')
                        if t:
                            date_iso = self.parse_swedish_date(t.get_text(strip=True))
                except Exception:
                    pass

                if not date_iso:
                    # hoppa om vi inte kan tolka datum
                    continue

                if not self.is_relevant(title):
                    continue

                events.append(self.event(
                    title=title,
                    date_iso=date_iso,
                    url=href,
                    description='',
                    categories=["biodiv", "mat"]
                ))
        except Exception as e:
            print(f"Error in {self.name}: {e}")
        return events
