from .base import BaseScraper

class EnergimyndighetenScraper(BaseScraper):
    name = "Energimyndigheten"
    source_id = "energimyndigheten"
    base_url = "https://www.energimyndigheten.se"
    EVENTS_URL = "https://www.energimyndigheten.se/om-oss/press-och-kanaler/kalender/"
    
    def fetch(self) -> list[dict]:
        events = []
        try:
            from bs4 import BeautifulSoup
            
            soup = self.soup(self.EVENTS_URL)
            
            # Event-länkar är strukturerade som: <a>Titel - Kategori - Datum Tid</a>
            for link in soup.select('a[href*="/kalender/"]'):
                full_text = link.get_text(strip=True)
                href = link.get('href', '')
                
                if not href or href == '/':
                    continue
                
                # Lägg till base_url om det är en relativ länk
                if not href.startswith('http'):
                    href = self.base_url + href
                
                # Exempel: "Dialogmöte laddinfrastruktur - Seminarier - 10 mars 10:00-15:00"
                parts = full_text.split(' - ')
                if len(parts) < 2:
                    continue
                
                title = parts[0].strip()
                if not title or len(title) < 5:
                    continue
                
                # Försök extrahera datum från länktext
                date_iso = self.parse_swedish_date(full_text)
                if not date_iso:
                    continue
                
                if not self.is_relevant(title):
                    continue
                
                events.append(self.event(
                    title=title,
                    date_iso=date_iso,
                    url=href,
                    description='',
                    categories=["energi", "klimat"]
                ))
        
        except Exception as e:
            print(f"Error in {self.name}: {e}")
        
        return events
