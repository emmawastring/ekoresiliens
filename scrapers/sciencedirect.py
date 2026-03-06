import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import time

def fetch_sciencedirect_articles():
    """
    Fetch open access articles from ScienceDirect based on various sustainability topics.
    Note: ScienceDirect has strong anti-bot protection and may block automated requests.
    This function currently returns empty results due to access restrictions.
    """
    print("ScienceDirect scraping is currently blocked by anti-bot protection.")
    print("Consider manual collection or using ScienceDirect's official APIs.")
    return []

def parse_sciencedirect_article(container, base_url, categories, query):
    try:
        # Extract title
        title_elem = container.select_one("h2, .article-title, .result-title, a[href*='/science/article/']")
        if not title_elem:
            return None

        title = title_elem.get_text(strip=True)
        if not title:
            return None

        # Extract URL
        url_elem = title_elem if title_elem.name == 'a' else container.select_one("a[href*='/science/article/']")
        url = url_elem['href'] if url_elem else ""
        if url and not url.startswith('http'):
            url = urljoin(base_url, url)

        # Extract authors
        authors_elem = container.select_one(".author, .authors, .article-authors")
        authors = authors_elem.get_text(strip=True) if authors_elem else ""

        # Extract journal/publication info
        journal_elem = container.select_one(".publication, .journal, .source-title")
        journal = journal_elem.get_text(strip=True) if journal_elem else ""

        # Extract abstract/snippet if available
        abstract_elem = container.select_one(".abstract, .snippet, .article-description")
        abstract = abstract_elem.get_text(strip=True)[:300] + "..." if abstract_elem else ""

        # Create description
        description = f"Open access article from ScienceDirect"
        if authors:
            description += f" by {authors}"
        if journal:
            description += f" in {journal}"
        if abstract:
            description += f". {abstract}"

        # Generate unique ID
        article_id = f"sd_{hash(url or title)}_{hash(query)}"

        return {
            "id": article_id,
            "title": title,
            "source": "ScienceDirect",
            "source_name": "ScienceDirect Open Access",
            "type": "artikel",
            "icon": "📄",
            "url": url,
            "cats": categories,
            "desc": description
        }

    except Exception as e:
        print(f"Error parsing ScienceDirect article: {e}")
        return None