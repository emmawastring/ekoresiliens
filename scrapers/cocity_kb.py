import requests
from bs4 import BeautifulSoup
import re

def fetch_cocity_resources():
    """
    Fetch resources from CoCity (tools, reports, examples).
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://www.cocity.se"
    resources = []

    # Define the sections to scrape
    sections = [
        ("verktyg", "Verktyg", ["verktyg", "samhalle"]),
        ("rapporter-och-vagledningar", "Rapporter och vägledningar", ["rapport", "samhalle"]),
        ("exempel", "Exempel", ["guide", "samhalle"])
    ]

    for section_slug, section_name, categories in sections:
        try:
            url = f"{base_url}/{section_slug}/"
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find resource links
            resource_selectors = [
                'a[href*="/verktyg/"]',
                'a[href*="/rapporter-och-vagledningar/"]',
                'a[href*="/exempel/"]',
                '.resource-link a',
                '.card a',
                'article a'
            ]

            found_resources = []
            for selector in resource_selectors:
                found_resources.extend(soup.select(selector))
                if found_resources:
                    break

            for link in found_resources[:15]:  # Limit per section
                resource = parse_cocity_resource(link, base_url, categories, section_name)
                if resource:
                    resources.append(resource)

        except Exception as e:
            print(f"Error fetching CoCity {section_name}: {e}")
            continue

    return resources

def parse_cocity_resource(link_elem, base_url, categories, section_name):
    try:
        title = link_elem.get_text(strip=True)
        if not title or len(title) < 5:
            return None

        url = link_elem['href']
        if not url.startswith('http'):
            url = base_url + url

        # Enhance categories based on content keywords
        enhanced_cats = categories.copy()
        title_lower = title.lower()

        if any(word in title_lower for word in ["klimat", "climate", "hållbar", "sustainable"]):
            enhanced_cats.append("klimat")
        if any(word in title_lower for word in ["natur", "nature", "grön", "green", "biodiversity"]):
            enhanced_cats.append("biodiv")
        if any(word in title_lower for word in ["vatten", "water", "flood", "blue-green"]):
            enhanced_cats.append("vatten")
        if any(word in title_lower for word in ["energi", "energy", "renewable"]):
            enhanced_cats.append("energi")

        # Determine icon based on section
        icon = "🛠️" if "verktyg" in section_name.lower() else "📊" if "rapport" in section_name.lower() else "💡"

        return {
            "id": f"cocity_{hash(url)}_{hash(section_name)}",
            "title": title,
            "source": "CoCity",
            "source_name": "CoCity",
            "type": "verktyg" if "verktyg" in section_name.lower() else "rapport" if "rapport" in section_name.lower() else "guide",
            "icon": icon,
            "url": url,
            "cats": list(set(enhanced_cats)),  # Remove duplicates
            "desc": f"Från CoCity {section_name}: {title}"
        }

    except Exception as e:
        print(f"Error parsing CoCity resource: {e}")
        return None