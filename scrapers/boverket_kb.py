import requests
from bs4 import BeautifulSoup
import re

def fetch_boverket_pbl_resources():
    """
    Fetch PBL knowledge bank themes from Boverket.
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://www.boverket.se"
    resources = []

    try:
        url = f"{base_url}/sv/PBL-kunskapsbanken/teman/"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find theme links
        theme_links = soup.select('a[href*="/sv/PBL-kunskapsbanken/teman/"]')

        for link in theme_links:
            theme = parse_boverket_theme(link, base_url)
            if theme:
                resources.append(theme)

    except Exception as e:
        print(f"Error fetching Boverket PBL resources: {e}")

    return resources

def parse_boverket_theme(link_elem, base_url):
    try:
        title = link_elem.get_text(strip=True)
        if not title or len(title) < 5:
            return None

        url = link_elem['href']
        if not url.startswith('http'):
            url = base_url + url

        # Determine categories based on title keywords
        categories = ["omstallning", "policy"]  # Default for planning/building
        title_lower = title.lower()

        if any(word in title_lower for word in ["klimat", "climate", "hållbar", "sustainable"]):
            categories.append("klimat")
        if any(word in title_lower for word in ["natur", "nature", "grön", "green"]):
            categories.append("biodiv")
        if any(word in title_lower for word in ["vatten", "water", "flood"]):
            categories.append("vatten")
        if any(word in title_lower for word in ["energi", "energy"]):
            categories.append("energi")

        return {
            "id": f"boverket_{hash(url)}",
            "title": title,
            "source": "Boverket",
            "source_name": "Boverket PBL",
            "type": "guide",
            "icon": "🏛️",
            "url": url,
            "cats": list(set(categories)),  # Remove duplicates
            "desc": f"PBL-kunskapsbanken från Boverket: {title}"
        }

    except Exception as e:
        print(f"Error parsing Boverket theme: {e}")
        return None