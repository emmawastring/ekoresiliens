import requests
from bs4 import BeautifulSoup
import re

def fetch_millennium_assessment_resources():
    """
    Fetch resources from Millennium Ecosystem Assessment.
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://www.millenniumassessment.org"
    resources = []

    # Define the sections to scrape
    sections = [
        ("en/Condition.html", "Condition", ["biodiv", "omstallning"]),
        ("en/Scenarios.html", "Scenarios", ["klimat", "omstallning"]),
        ("en/Responses.html", "Responses", ["policy", "omstallning"])
    ]

    for section_path, section_name, categories in sections:
        try:
            url = f"{base_url}/{section_path}"
            response = requests.get(url, timeout=15)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Find resource links and content
            resource_links = soup.select('a[href*=".pdf"], a[href*=".doc"], a[href*="report"], a[href*="assessment"]')

            for link in resource_links[:10]:  # Limit per section
                resource = parse_ma_resource(link, base_url, categories, section_name)
                if resource:
                    resources.append(resource)

            # Also look for main content sections
            content_sections = soup.select('.content h2, .content h3, .main-content h2, .main-content h3')
            for section in content_sections[:5]:
                resource = parse_ma_section(section, url, categories, section_name)
                if resource:
                    resources.append(resource)

        except Exception as e:
            print(f"Error fetching Millennium Assessment {section_name}: {e}")
            continue

    return resources

def parse_ma_resource(link_elem, base_url, categories, section_name):
    try:
        title = link_elem.get_text(strip=True)
        if not title or len(title) < 5:
            return None

        url = link_elem['href']
        if not url.startswith('http'):
            url = base_url + url

        return {
            "id": f"ma_{hash(url)}_{hash(section_name)}",
            "title": f"Millennium Assessment: {title}",
            "source": "Millennium Assessment",
            "source_name": "Millennium Ecosystem Assessment",
            "type": "rapport",
            "icon": "🌍",
            "url": url,
            "cats": categories,
            "desc": f"Millennium Ecosystem Assessment - {section_name} section: {title}"
        }

    except Exception as e:
        print(f"Error parsing MA resource: {e}")
        return None

def parse_ma_section(section_elem, page_url, categories, section_name):
    try:
        title = section_elem.get_text(strip=True)
        if not title or len(title) < 5:
            return None

        return {
            "id": f"ma_section_{hash(page_url + title)}_{hash(section_name)}",
            "title": f"Millennium Assessment - {section_name}: {title}",
            "source": "Millennium Assessment",
            "source_name": "Millennium Ecosystem Assessment",
            "type": "artikel",
            "icon": "📖",
            "url": page_url,
            "cats": categories,
            "desc": f"Millennium Ecosystem Assessment content section: {title}"
        }

    except Exception as e:
        print(f"Error parsing MA section: {e}")
        return None