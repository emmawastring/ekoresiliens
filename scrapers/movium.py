"""SLU Movium – hämtar via sökendpoint"""
import requests
import re
from bs4 import BeautifulSoup
from .base import BaseScraper

SOURCE_NAME = "SLU Movium"
BASE_URL    = "https://movium.slu.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

SEARCH_TERMS = ["webbinarium", "kurs", "konferens", "seminarium", "workshop"]

class MoviumScraper(BaseScraper):
    name      = SOURCE_NAME
    source_id = "MOVIUM"

    def fetch(self) -> list[dict]:
        events = []
        seen_urls = set()

        for term in SEARCH_TERMS:
            page = 1
            while True:
                url = f"{BASE_URL}/soek/?q={term}&page={page}"
                try:
                    r = requests.get(url, headers=HEADERS, timeout=15)
                    r.raise_for_status()
                    soup = BeautifulSoup(r.text, "html.parser")

                    # Sökresultat är <a class="block group ...">
                    results = soup.find_all("a", class_="block", href=True)
                    if not results:
                        break

                    found_any = False
                    for a in results:
                        # Kolla att det är Kalendarium
                        type_el = a.find("p", class_=lambda c: c and "uppercase" in c)
                        if not type_el:
                            continue
                        type_text = type_el.get_text(strip=True).lower()
                        if "kalendarium" not in type_text:
                            continue

                        # Datum – andra p.uppercase
                        ps = a.find_all("p", class_=lambda c: c and "uppercase" in c)
                        date_iso = None
                        for p in ps:
                            m = re.search(r"(\d{4}-\d{2}-\d{2})", p.get_text())
                            if m:
                                date_iso = m.group(1)
                                break
                        if not date_iso:
                            continue

                        # Titel
                        h2 = a.find("h2")
                        if not h2:
                            continue
                        title = h2.get_text(strip=True)

                        # URL
                        href = a["href"]
                        if not href.startswith("http"):
                            href = BASE_URL + href
                        if href in seen_urls:
                            continue
                        seen_urls.add(href)

                        # Beskrivning
                        desc_el = a.find("p", class_=lambda c: c and "line-clamp" in c)
                        desc = desc_el.get_text(strip=True) if desc_el else ""

                        events.append(self.event(
                            title=title,
                            date_iso=date_iso,
                            url=href,
                            description=desc,
                            categories=["omstallning", "samhalle"],
                        ))
                        found_any = True

                    if not found_any:
                        break
                    page += 1

                except Exception as e:
                    print(f"  {SOURCE_NAME}: fel ({term} s{page}): {e}")
                    break

        return events