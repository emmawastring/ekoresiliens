"""Under Ekarna – event-scraper (På gång) + KB (Förädling, Historia)"""
import requests
import re
from bs4 import BeautifulSoup
from .base import BaseScraper

SOURCE_NAME = "Under Ekarna"
BASE_URL    = "https://www.underekarna.se"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

SWEDISH_MONTHS = {
    "januari":1,"februari":2,"mars":3,"april":4,"maj":5,"juni":6,
    "juli":7,"augusti":8,"september":9,"oktober":10,"november":11,"december":12
}

def parse_date(text):
    """Parsar datum ur text som '4 mars 2026 kl.18.30'"""
    text = text.lower()
    m = re.search(r'(\d{1,2})\s+([a-zåäö]+)\s+(\d{4})', text)
    if m:
        day   = int(m.group(1))
        month = SWEDISH_MONTHS.get(m.group(2))
        year  = int(m.group(3))
        if month:
            return f"{year}-{month:02d}-{day:02d}"
    return None

class UnderekarnaScraper(BaseScraper):
    name      = SOURCE_NAME
    source_id = "underekarna"

    def fetch(self) -> list[dict]:
        events = []
        try:
            r = requests.get(f"{BASE_URL}/p%C3%A5-g%C3%A5ng/", headers=HEADERS, timeout=15)
            r.encoding = "utf-8"
            soup = BeautifulSoup(r.text, "html.parser")

            # Event-block: h5 följt av p med datum
            for h5 in soup.find_all("h5"):
                title = h5.get_text(strip=True)
                if not title:
                    continue

                # Hämta nästa syskon-p
                desc = ""
                date_iso = None
                url = f"{BASE_URL}/p%C3%A5-g%C3%A5ng/"

                # Gå igenom efterföljande siblings
                for sib in h5.find_next_siblings():
                    if sib.name == "h5":
                        break
                    if sib.name == "p":
                        text = sib.get_text(" ", strip=True)
                        if not date_iso:
                            date_iso = parse_date(text)
                        desc += text + " "
                        # Hämta eventuell anmälningslänk
                        a = sib.find("a", href=True)
                        if a and "http" in a["href"]:
                            url = a["href"]

                if date_iso:
                    events.append(self.event(
                        title=title,
                        date_iso=date_iso,
                        url=url,
                        description=desc.strip(),
                        categories=["skog", "agroforestry", "beredskap", "mat"],
                    ))
        except Exception as e:
            print(f"  {SOURCE_NAME}: fel events: {e}")

        return events