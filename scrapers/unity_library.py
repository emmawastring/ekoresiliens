"""Scraper for United Diversity library resources"""

import re
from bs4 import BeautifulSoup
import requests


def fetch_unity_library_resources():
    """Fetch resources from United Diversity Library"""
    resources = []
    
    # Different sections and their category mappings
    sections = [
        ("https://library.uniteddiversity.coop/More_Books_and_Reports/", ["samhalle"], "Böcker och rapporter"),
        ("https://library.uniteddiversity.coop/Permaculture/", ["skogstradgard", "agroforestry"], "Permakultur"),
        ("https://library.uniteddiversity.coop/Permaculture/Agroforestry/", ["agroforestry"], "Agroforestry"),
        ("https://library.uniteddiversity.coop/Permaculture/Agroforestry/Forest_Gardens/", ["skogstradgard"], "Skogsträdgård"),
        ("https://library.uniteddiversity.coop/Beekeeping/", ["biodiv"], "Bisamhälle"),
        ("https://library.uniteddiversity.coop/Climate_Change/", ["klimat"], "Klimatförändringar"),
    ]
    
    for url, cats, desc in sections:
        try:
            resp = requests.get(url, timeout=10)
            soup = BeautifulSoup(resp.content, 'html.parser')
            
            # Find all links to PDFs and documents
            for link in soup.find_all('a', href=True):
                href = link.get('href', '')
                title = link.get_text(strip=True)
                
                # Skip empty or non-relevant links
                if not title or len(title) < 3:
                    continue
                
                # Filter for actual content links
                if any(x in href.lower() for x in ['.pdf', '.doc', '.html', 'library']) or href.startswith('/'):
                    if not href.startswith('http'):
                        href = "https://library.uniteddiversity.coop" + href
                    
                    resources.append({
                        "id": f"udl_{len(resources)}",
                        "source": "UDL",
                        "source_name": "United Diversity Library",
                        "type": "rapport",
                        "icon": "📚",
                        "title": title,
                        "desc": f"{desc}",
                        "cats": cats,
                        "url": href
                    })
        
        except Exception as e:
            print(f"Error fetching from {url}: {e}")
    
    return resources


if __name__ == '__main__':
    results = fetch_unity_library_resources()
    print(f"Found {len(results)} United Diversity Library resources")
    for r in results[:5]:
        print(f"  - {r['title']}")
