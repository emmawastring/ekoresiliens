"""
Scraper for Holma Folkhögskola courses
https://www.holmafolkhogskola.se/kurser/
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re
from .base import BaseScraper


class HolmaScraper(BaseScraper):
    SOURCE_ID   = "holma"
    SOURCE_NAME = "Holma Folkhögskola"
    BASE_URL    = "https://www.holmafolkhogskola.se"
    COURSES_URL = "https://www.holmafolkhogskola.se/kurser/"

    # Profilkurs-undersidor att scrapa
    COURSE_PATHS = [
        "/profilkurs/hallbar-matlagning-med-lokala-ravaror/",
        "/profilkurs/hantverk-fordjupning/",
        "/profilkurs/inre-omstallning-i-kontakt-med-jorden-andra-och-hela-dig/",
        "/profilkurs/skogstradgard-och-smaskalig-agroforestry/",
        "/profilkurs/seniorkurs-odling-matlagning-och-gemenskap/",
        "/profilkurs/hantverk-for-sjalvhushallare/",
        "/profilkurs/mat-ur-jorden/",
        "/profilkurs/sociokrati-och-sjalvorganiserat-samarbete-distans/",
        "/profilkurs/livsmedelsforadling-for-omstallare/",
        "/profilkurs/notodling-for-sydsvenska-forhallande-25-distans/",
        "/profilkurs/permakulturdesign-pdc/",
        "/profilkurs/froodling-distans/",
        "/oppet-program/skordefest/",
        "/oppet-program/oppet-hus/",
        "/oppet-program/holmasommar/",
    ]

    def fetch(self):
        events = []
        headers = {"User-Agent": "Mozilla/5.0 (compatible; Ekoresiliens/1.0)"}

        for path in self.COURSE_PATHS:
            url = self.BASE_URL + path
            try:
                r = requests.get(url, headers=headers, timeout=15)
                if r.status_code != 200:
                    continue
                soup = BeautifulSoup(r.text, "html.parser")

                # Titel
                h1 = soup.find("h1")
                title = h1.get_text(strip=True) if h1 else path.strip("/").split("/")[-1]

                # Beskrivning - första stycket i innehållet
                content_div = soup.find("div", class_="entry-content") or soup.find("article")
                description = ""
                if content_div:
                    paras = content_div.find_all("p")
                    for p in paras:
                        txt = p.get_text(strip=True)
                        if len(txt) > 50:
                            description = txt[:300]
                            break

                # Datum - leta efter datum i texten (format: dag månad år)
                date_iso = None
                months = {
                    "januari": "01", "februari": "02", "mars": "03", "april": "04",
                    "maj": "05", "juni": "06", "juli": "07", "augusti": "08",
                    "september": "09", "oktober": "10", "november": "11", "december": "12"
                }
                page_text = soup.get_text()
                # Sök efter "start: DD månad YYYY" eller "DD månad YYYY"
                date_patterns = [
                    r'(\d{1,2})\s+(januari|februari|mars|april|maj|juni|juli|augusti|september|oktober|november|december)\s+(\d{4})',
                    r'(\d{4})-(\d{2})-(\d{2})',
                ]
                for pat in date_patterns:
                    m = re.search(pat, page_text, re.IGNORECASE)
                    if m:
                        if len(m.groups()) == 3 and not m.group(1).isdigit() or len(m.group(1)) == 4:
                            # YYYY-MM-DD format
                            date_iso = m.group(0)
                        else:
                            day = m.group(1).zfill(2)
                            month = months.get(m.group(2).lower(), "01")
                            year = m.group(3)
                            date_iso = f"{year}-{month}-{day}"
                        break

                # Om inget datum hittas, sätt till framtida okänt datum
                if not date_iso:
                    date_iso = f"{datetime.now().year + 1}-01-01"

                # Plats
                location = "Höör, Skåne"
                if "distans" in path.lower():
                    location = "Online"

                # Kategorier
                categories = ["mat", "agroforestry"]
                if "skog" in path.lower() or "odling" in path.lower():
                    categories = ["agroforestry", "mat"]
                elif "hantverk" in path.lower():
                    categories = ["mat"]
                elif "permakultur" in path.lower():
                    categories = ["agroforestry", "biodiv"]
                elif "fest" in path.lower() or "hus" in path.lower() or "sommar" in path.lower():
                    categories = ["samhalle"]

                events.append(self.event(
                    title=title,
                    date=date_iso,
                    url=url,
                    description=description,
                    categories=categories,
                    source_name=self.SOURCE_NAME,
                ))

            except Exception as e:
                print(f"  Holma: fel för {path}: {e}")

        return events