from .base import BaseScraper

class KlimatriksdagenScraper(BaseScraper):
    name = "Klimatriksdagen"
    source_id = "klimatriksdagen"
    base_url = "https://klimatriksdagen.se"
    EVENTS_URL = "https://klimatriksdagen.se/aktuellt/"
    
    def fetch(self) -> list[dict]:
        events = []
        try:
            import requests
            from bs4 import BeautifulSoup
            
            response = requests.get(self.EVENTS_URL, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Find event containers
            for item in soup.select('article, .event, li'):
                title_elem = item.select_one('h2, h3, a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                
                # Skip non-event items
                if not self.is_relevant(title):
                    continue
                
                # Extract date
                date_elem = item.select_one('time, .date, [data-date]')
                date_text = date_elem.get_text(strip=True) if date_elem else ""
                date_iso = self.parse_swedish_date(date_text + " " + title)
                
                # Extract description
                desc_elem = item.select_one('p, .excerpt, .description')
                description = desc_elem.get_text(strip=True) if desc_elem else ""
                
                # Extract URL
                link_elem = item.select_one('a[href]')
                url = link_elem['href'] if link_elem else ""
                if url and not url.startswith('http'):
                    url = self.base_url + url
                
                if date_iso:
                    events.append(self.event(
                        title=title,
                        date_iso=date_iso,
                        url=url,
                        description=description,
                        categories=["klimat", "samhalle", "policy"]
                    ))
        
        except Exception as e:
            print(f"Error in {self.name}: {e}")
        
        return events
