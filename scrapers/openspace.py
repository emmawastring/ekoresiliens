from scrapers.base import BaseScraper
import re
from datetime import datetime

class OpenSpaceConsultingScraper(BaseScraper):
    name = "Open Space Consulting"
    source_id = "openspace"
    base_url = "https://openspaceconsulting.com"

    def fetch(self):
        try:
            soup = self.soup("https://openspaceconsulting.com/kategori/aktiviteter/kommande-aktiviteter/")
            events = []

            # Look for event containers
            event_containers = soup.select("article, .event-item, .post, .entry")

            for container in event_containers:
                event = self.parse_event(container)
                if event:
                    events.append(event)

            return events
        except Exception as e:
            print(f"Open Space Consulting error: {e}")
            return []

    def parse_event(self, container):
        try:
            # Extract title
            title_elem = container.select_one("h1, h2, h3, .entry-title, .post-title")
            if not title_elem:
                return None
            title = title_elem.get_text(strip=True)

            # Extract URL
            url_elem = container.select_one("a[href*='/event/'], a[href*='/aktivitet/']")
            if not url_elem:
                url_elem = title_elem if title_elem.name == 'a' else container.select_one("a")
            url = url_elem['href'] if url_elem else ""
            if not url.startswith('http'):
                url = self.base_url + url

            # Extract date - look for various date patterns
            date_text = ""
            date_elem = container.select_one("time, .date, .event-date, .entry-date")
            if date_elem:
                date_text = date_elem.get_text(strip=True)
                if not date_text:
                    date_text = date_elem.get('datetime', '')

            # If no date found, try to extract from text
            if not date_text:
                text_content = container.get_text()
                # Look for Swedish date patterns
                date_patterns = [
                    r'(\d{1,2})\s*(januari|februari|mars|april|maj|juni|juli|augusti|september|oktober|november|december)\s*(\d{4})',
                    r'(\d{4})-(\d{2})-(\d{2})',
                    r'(\d{1,2})/(\d{1,2})/(\d{4})'
                ]
                for pattern in date_patterns:
                    match = re.search(pattern, text_content, re.IGNORECASE)
                    if match:
                        date_text = match.group()
                        break

            # Parse date
            date_iso = self.parse_swedish_date(date_text)
            if not date_iso:
                return None  # Skip events without dates

            # Extract time if available
            time = ""
            time_match = re.search(r'(\d{1,2}:\d{2})', container.get_text())
            if time_match:
                time = time_match.group(1)

            # Extract description
            desc_elem = container.select_one(".entry-content, .post-content, .event-description, p")
            description = desc_elem.get_text(strip=True)[:200] + "..." if desc_elem else ""

            # Determine categories based on content
            categories = ["omstallning"]  # Default category
            text_lower = (title + " " + description).lower()

            if any(word in text_lower for word in ["klimat", "climate", "miljö", "environment"]):
                categories.append("klimat")
            if any(word in text_lower for word in ["biodiversitet", "biodiversity", "natur", "nature"]):
                categories.append("biodiv")
            if any(word in text_lower for word in ["jordbruk", "agriculture", "lantbruk"]):
                categories.append("mat")
            if any(word in text_lower for word in ["stad", "urban", "kommun"]):
                categories.append("omstallning")

            return {
                "id": f"openspace_{hash(title + date_iso)}",
                "title": title,
                "date_iso": date_iso,
                "time": time,
                "url": url,
                "source_id": self.source_id,
                "categories": list(set(categories)),  # Remove duplicates
                "free": True,  # Assume free unless specified otherwise
                "description": description
            }

        except Exception as e:
            print(f"Error parsing Open Space event: {e}")
            return None