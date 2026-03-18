"""Studiefrämjandet – kurser och evenemang"""
import requests, re, json
from .base import BaseScraper

class StudieframjandetScraper(BaseScraper):
    SOURCE_ID   = "studieframjandet"
    source_id   = "studieframjandet"
    SOURCE_NAME = "Studiefrämjandet"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.studieframjandet.se"

    # Topic-IDs för relevanta ämnen
    TOPICS = [
        ("702", ["mat", "biodiv"]),       # Natur & trädgård
        ("703", ["mat"]),                  # Mathantverk
        ("704", ["omstallning"]),          # Hållbarhet
        ("801", ["mat"]),                  # Odling
    ]

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        events = []
        seen = set()

        for topic_id, cats in self.TOPICS:
            url = (
                f"https://www.studieframjandet.se/kurssok/"
                f"?topicFilter=%5B%22{topic_id}%22%5D"
                f"&miscFilter=%5B%22Visa%20distans%20och%20p%C3%A5%20plats%22%5D"
                f"&page=1"
            )
            try:
                r = requests.get(url, headers=h, timeout=15)
                r.encoding = "utf-8"
                # Parsa JSON-objekt inbäddade i HTML
                pattern = r'"Text":"(.*?)","HitText":.*?"Url":"(.*?)",".*?"Location":"(.*?)","Date":"(202[0-9]-\d{2}-\d{2})","Times":\d+,"Time":"(.*?)"'
                for m in re.finditer(pattern, r.text):
                    title    = m.group(1)
                    url_path = m.group(2)
                    location = m.group(3)
                    date     = m.group(4)
                    time     = m.group(5)

                    if url_path in seen:
                        continue
                    seen.add(url_path)

                    full_url = self.BASE_URL + url_path if url_path.startswith('/') else url_path
                    desc = f"Plats: {location}" if location else ""

                    events.append(self.event(
                        title=title,
                        date_iso=date,
                        url=full_url,
                        description=desc,
                        categories=cats,
                        time=time,
                    ))
            except Exception as e:
                self.log(f"FEL topic {topic_id}: {e}")

        return events