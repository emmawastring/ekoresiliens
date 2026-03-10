import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin

def fetch_slu_publications():
    """
    Fetch open access publications from SLU.
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://publications.slu.se"
    resources = []

    try:
        # The URL provided has specific filters for open access publications
        url = f"{base_url}/?file=orga%2Fshow&sort=PY%20desc%2Cslu_last_update%20desc&cid=259094082&lang=se&fq[]=%7B!tag%3Dpubl_type_se%7D(publ_type_se%3A%22Doktorsavhandling%22%20OR%20publ_type_se%3A%22Bok%22%20OR%20publ_type_se%3A%22Faktablad%22%20OR%20publ_type_se%3A%22Forskningsartikel%22%20OR%20publ_type_se%3A%22Rapport%22%20OR%20publ_type_se%3A%22Tidningsartikel%22%20OR%20publ_type_se%3A%22Annat%20bidrag%20i%20vetenskaplig%20tidskrift%22%20OR%20publ_type_se%3A%22Kapitel%20i%20rapport%20%22%20OR%20publ_type_se%3A%22%C3%96vrig%20publikation%22%20OR%20publ_type_se%3A%22Bokkapitel%22)&fq[]=%7B!tag%3Doa_status_se%7D(oa_status_se%3A%22Visa%20endast%20%C3%B6ppet%20inneh%C3%A5ll%22)"

        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find publication entries
        publication_entries = soup.select('.publication-entry, .result-item, article, .pub-item')

        for entry in publication_entries[:20]:  # Limit to 20 publications
            pub = parse_slu_publication(entry, base_url)
            if pub:
                resources.append(pub)

    except Exception as e:
        print(f"Error fetching SLU publications: {e}")

    return resources

def parse_slu_publication(entry_elem, base_url):
    try:
        # Find title
        title_elem = entry_elem.select_one('h3, .title, .pub-title, a[href*="/show/"]')
        if not title_elem:
            return None

        title = title_elem.get_text(strip=True)
        if not title:
            return None

        # Find URL
        url_elem = title_elem if title_elem.name == 'a' else entry_elem.select_one('a[href*="/show/"]')
        url = urljoin(base_url, url_elem['href']) if url_elem else ""

        # Find authors
        authors_elem = entry_elem.select_one('.authors, .author, .creator')
        authors = authors_elem.get_text(strip=True) if authors_elem else ""

        # Find publication type
        type_elem = entry_elem.select_one('.type, .pub-type, .document-type')
        pub_type = type_elem.get_text(strip=True) if type_elem else "publikation"

        # Find year
        year_elem = entry_elem.select_one('.year, .pub-year, .date')
        year = year_elem.get_text(strip=True) if year_elem else ""

        # Determine categories based on content
        categories = ["omstallning"]  # Default for SLU publications
        text_content = (title + " " + authors).lower()

        if any(word in text_content for word in ["klimat", "climate", "hållbar", "sustainable", "miljö", "environment"]):
            categories.append("klimat")
        if any(word in text_content for word in ["natur", "nature", "biodiversity", "biodiv", "ekosystem", "ecosystem"]):
            categories.append("biodiv")
        if any(word in text_content for word in ["jordbruk", "agriculture", "lantbruk", "farming"]):
            categories.append("mat")
        if any(word in text_content for word in ["skog", "forest", "forestry"]):
            categories.append("skog")
        if any(word in text_content for word in ["vatten", "water", "marine", "hav"]):
            categories.append("vatten")
        if any(word in text_content for word in ["energi", "energy", "renewable"]):
            categories.append("energi")

        # Map publication type to our types
        type_mapping = {
            "doktorsavhandling": "rapport",
            "bok": "bok",
            "faktablad": "guide",
            "forskningsartikel": "artikel",
            "rapport": "rapport",
            "tidningsartikel": "artikel",
            "annat bidrag": "artikel",
            "kapitel i rapport": "artikel",
            "övrig publikation": "artikel",
            "bokkapitel": "artikel"
        }

        resource_type = "artikel"  # default
        for key, value in type_mapping.items():
            if key.lower() in pub_type.lower():
                resource_type = value
                break

        # Create description
        desc = f"SLU publikation"
        if authors:
            desc += f" av {authors}"
        if year:
            desc += f" ({year})"
        desc += f" - {pub_type}"

        return {
            "id": f"slu_pub_{hash(url or title)}",
            "title": title,
            "source": "SLU",
            "source_name": "Sveriges lantbruksuniversitet",
            "type": resource_type,
            "icon": "📚",
            "url": url,
            "cats": list(set(categories)),
            "desc": desc
        }

    except Exception as e:
        print(f"Error parsing SLU publication: {e}")
        return None