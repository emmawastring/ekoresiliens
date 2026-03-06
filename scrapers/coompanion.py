from .base import BaseScraper
import re


class CoompanionScraper(BaseScraper):
    name = "Coompanion"
    source_id = "Coompanion"
    base_url = "https://coompanion.se"
    EVENTS_URL = "https://coompanion.se/alla-event/"
    
    def fetch(self) -> list[dict]:
        events = []
        try:
            soup = self.soup(self.EVENTS_URL)
            
            # Scrape event links and details
            for item in soup.select('a[href*="/event/"], .event-item, article'):
                title_elem = item.select_one('h2, h3, .event-title, a')
                if not title_elem:
                    continue
                
                title = title_elem.get_text(strip=True)
                if not title or len(title) < 5:
                    continue
                
                # Get URL
                link = item.select_one('a[href]')
                url = link.get('href', '') if link else ''
                if not url:
                    url = item.get('href', '')
                
                if not url.startswith('http'):
                    url = self.base_url + url
                
                # Extract date from text or nearby elements
                date_text = item.get_text(' ', strip=True)
                date_iso = self.parse_swedish_date(date_text)
                
                if not date_iso:
                    # Try looking at datetime attributes
                    time_elem = item.select_one('time, [datetime]')
                    if time_elem:
                        attr = time_elem.get('datetime') or time_elem.get_text(strip=True)
                        date_iso = self.parse_swedish_date(attr)
                
                if not date_iso:
                    continue
                
                if not self.is_relevant(title):
                    continue
                
                events.append(self.event(
                    title=title,
                    date_iso=date_iso,
                    url=url,
                    description='',
                    categories=["samhalle", "mat"]
                ))
        
        except Exception as e:
            print(f"Error in {self.name}: {e}")
        
        return events
