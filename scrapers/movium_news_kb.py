import requests
from bs4 import BeautifulSoup
import re

def fetch_movium_news():
    """
    Fetch all news from SLU MOVIUM.
    Returns a list of knowledge resource dictionaries.
    """
    base_url = "https://movium.slu.se"
    resources = []

    try:
        url = f"{base_url}/nyheter/#alla"
        response = requests.get(url, timeout=15)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find news article links
        news_links = soup.select('a[href*="/nyheter/"], .news-item a, .article-link, article a')

        for link in news_links[:30]:  # Limit to 30 news items
            news = parse_movium_news(link, base_url)
            if news:
                resources.append(news)

    except Exception as e:
        print(f"Error fetching MOVIUM news: {e}")

    return resources

def parse_movium_news(link_elem, base_url):
    try:
        title = link_elem.get_text(strip=True)
        if not title or len(title) < 5:
            return None

        url = link_elem['href']
        if not url.startswith('http'):
            url = base_url + url

        # Determine categories based on MOVIUM focus (urban green, landscape architecture)
        categories = ["omstallning", "biodiv"]  # Default categories
        title_lower = title.lower()

        if any(word in title_lower for word in ["klimat", "climate", "hållbar", "sustainable"]):
            categories.append("klimat")
        if any(word in title_lower for word in ["stad", "urban", "city", "kommun"]):
            categories.append("omstallning")
        if any(word in title_lower for word in ["grön", "green", "natur", "nature"]):
            categories.append("biodiv")
        if any(word in title_lower for word in ["skog", "forest", "träd", "trees"]):
            categories.append("skog")
        if any(word in title_lower for word in ["vatten", "water", "blue-green"]):
            categories.append("vatten")
        if any(word in title_lower for word in ["jordbruk", "agriculture", "farming"]):
            categories.append("mat")

        return {
            "id": f"movium_news_{hash(url)}",
            "title": title,
            "source": "SLU MOVIUM",
            "source_name": "SLU MOVIUM",
            "type": "artikel",
            "icon": "📰",
            "url": url,
            "cats": list(set(categories)),  # Remove duplicates
            "desc": f"Nyhet från SLU MOVIUM: {title}"
        }

    except Exception as e:
        print(f"Error parsing MOVIUM news: {e}")
        return None