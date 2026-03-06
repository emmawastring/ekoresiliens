import requests
from bs4 import BeautifulSoup
import re

def fetch_livsmedelsverket_resources():
    """
    Fetch publications from Livsmedelsverket.
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://www.livsmedelsverket.se"
    resources = []

    try:
        url = f"{base_url}/om-oss/publikationer/"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find publication links
        publication_links = soup.select('a[href*="/publikationer/"], a[href*="publication"], .publication a, .pub-item a')

        for link in publication_links[:25]:  # Limit to 25 publications
            pub = parse_lv_publication(link, base_url)
            if pub:
                resources.append(pub)

    except Exception as e:
        print(f"Error fetching Livsmedelsverket publications: {e}")

    return resources

def parse_lv_publication(link_elem, base_url):
    try:
        title = link_elem.get_text(strip=True)
        if not title or len(title) < 5:
            return None

        url = link_elem['href']
        if not url.startswith('http'):
            url = base_url + url

        # Determine categories - Livsmedelsverket focuses on food safety and nutrition
        categories = ["mat", "samhalle"]  # Default categories
        title_lower = title.lower()

        if any(word in title_lower for word in ["klimat", "climate", "hållbar", "sustainable", "miljö", "environment"]):
            categories.append("klimat")
        if any(word in title_lower for word in ["jordbruk", "agriculture", "lantbruk", "farming"]):
            categories.append("mat")
        if any(word in title_lower for word in ["hälsa", "health", "nutrition", "näring"]):
            categories.append("samhalle")
        if any(word in title_lower for word in ["policy", "regelverk", "regulation", "lag"]):
            categories.append("policy")

        return {
            "id": f"lv_{hash(url)}",
            "title": title,
            "source": "Livsmedelsverket",
            "source_name": "Livsmedelsverket",
            "type": "guide",
            "icon": "🥗",
            "url": url,
            "cats": list(set(categories)),  # Remove duplicates
            "desc": f"Publikation från Livsmedelsverket: {title}"
        }

    except Exception as e:
        print(f"Error parsing Livsmedelsverket publication: {e}")
        return None