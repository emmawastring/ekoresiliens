from .base import BaseScraper

class EkocentrumScraper(BaseScraper):
    name = "Ekocentrum"
    source_id = "ekocentrum"
    base_url = "https://www.ekocentrum.se"
    EVENTS_URL = "https://www.ekocentrum.se/kalendarium-start/"
    
    def fetch(self) -> list[dict]:
        events = []
        try:
            from bs4 import BeautifulSoup
            
            soup = self.soup(self.EVENTS_URL)
            
            # Event-titlar är i <h3><a>Titel</a></h3>, datum följer i nästa element
            for h3 in soup.select('h3'):
                link = h3.select_one('a')
                if not link:
                    continue
                
                title = link.get_text(strip=True)
                href = link.get('href', '')
                
                if not title or not href:
                    continue
                
                if not href.startswith('http'):
                    href = self.base_url + href
                
                # Försök hitta datum i följande sibling-element
                date_text = ""
                sibling = h3.find_next(['p', 'span', 'div'])
                if sibling:
                    date_text = sibling.get_text(strip=True)
                
                date_iso = self.parse_swedish_date(date_text + " " + title)
                if not date_iso:
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
