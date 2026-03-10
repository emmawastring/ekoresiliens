"""Scraper for MOVIUM SLU PDF resources"""

import re
from bs4 import BeautifulSoup
import requests


def fetch_movium_resources():
    """Fetch PDFs from MOVIUM nyheter section"""
    resources = []
    url = "https://movium.slu.se/nyheter/#PDF"
    
    try:
        resp = requests.get(url, timeout=10)
        soup = BeautifulSoup(resp.content, 'html.parser')
        
        # Find PDF links
        for link in soup.find_all('a', href=re.compile(r'\.pdf$', re.I)):
            title = link.get_text(strip=True)
            href = link.get('href', '')
            
            if not title or not href:
                continue
            
            if not href.startswith('http'):
                href = "https://movium.slu.se" + href
            
            resources.append({
                "id": f"movium_{len(resources)}",
                "source": "MOVIUM",
                "source_name": "SLU MOVIUM",
                "type": "rapport",
                "icon": "📄",
                "title": title,
                "desc": "PDF från SLU MOVIUM",
                "cats": ["omstallning", "biodiv"],
                "url": href
            })
    
    except Exception as e:
        print(f"Error fetching MOVIUM resources: {e}")
    
    return resources


if __name__ == '__main__':
    results = fetch_movium_resources()
    print(f"Found {len(results)} MOVIUM resources")
    for r in results[:3]:
        print(f"  - {r['title']}")
