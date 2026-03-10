import requests
from bs4 import BeautifulSoup
import re

def fetch_naturvardsverket_resources():
    """
    Fetch guidance and support resources from Naturvårdsverket.
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://www.naturvardsverket.se"
    resources = []

    # Categories from the URL
    categories = [
        ("Våtmark", ["vatten", "biodiv"]),
        ("Skyddad natur", ["biodiv", "omstallning"]),
        ("Samhällsplanering", ["omstallning", "policy"]),
        ("Miljömål och miljöledning", ["omstallning", "policy"]),
        ("Miljöbalken", ["policy", "omstallning"]),
        ("Luft och klimat", ["klimat", "omstallning"]),
        ("Invasiva främmande arter", ["biodiv"]),
        ("Allemansrätten", ["omstallning", "biodiv"]),
        ("Arter och artskydd", ["biodiv"]),
        ("Avlopp", ["vatten", "omstallning"]),
        ("Friluftsliv", ["omstallning", "biodiv"]),
        ("Förorenade områden", ["omstallning", "klimat"])
    ]

    for cat_name, cats in categories:
        try:
            # URL encode the category
            encoded_cat = cat_name.replace(" ", "%20").replace("å", "%C3%A5").replace("ä", "%C3%A4").replace("ö", "%C3%B6")
            url = f"{base_url}/vagledning-och-stod/?facets=Categories:{encoded_cat}"

            response = requests.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find resource links
            resource_links = soup.select('a[href*="/vagledning-och-stod/"]')

            for link in resource_links[:20]:  # Limit per category
                resource = parse_nv_resource(link, base_url, cats, cat_name)
                if resource:
                    resources.append(resource)

        except Exception as e:
            print(f"Error fetching NV resources for {cat_name}: {e}")
            continue

    return resources

def parse_nv_resource(link_elem, base_url, categories, category_name):
    try:
        title = link_elem.get_text(strip=True)
        if not title or len(title) < 10:
            return None

        url = link_elem['href']
        if not url.startswith('http'):
            url = base_url + url

        # Create resource object
        return {
            "id": f"nv_{hash(url)}_{hash(category_name)}",
            "title": title,
            "source": "Naturvårdsverket",
            "source_name": "Naturvårdsverket",
            "type": "guide",
            "icon": "📋",
            "url": url,
            "cats": categories,
            "desc": f"Vägledning från Naturvårdsverket inom kategori: {category_name}"
        }

    except Exception as e:
        print(f"Error parsing NV resource: {e}")
        return None