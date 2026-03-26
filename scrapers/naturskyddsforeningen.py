"""Naturskyddsföreningen – kalender"""
import requests, re, json
from .base import BaseScraper

class NaturskyddsforeningenScraper(BaseScraper):
    SOURCE_ID   = "naturskyddsforeningen"
    source_id   = "naturskyddsforeningen"
    SOURCE_NAME = "Naturskyddsföreningen"
    name        = SOURCE_NAME
    BASE_URL    = "https://www.naturskyddsforeningen.se"
    URL         = "https://www.naturskyddsforeningen.se/engagera-dig/kalender/"

    def fetch(self, date_iso=None):
        h = {"User-Agent": "Mozilla/5.0"}
        r = requests.get(self.URL, headers=h, timeout=15)
        r.encoding = "utf-8"

        events = []
        seen = set()

        # Data finns som JSON i HTML
        pattern = r'"id":\d+,"url":"(/engagera-dig/kalender/[^"]+)","title":"([^"]+)"'
        for m in re.finditer(pattern, r.text):
            url_path = m.group(1)
            title    = m.group(2)

            if url_path in seen:
                continue
            seen.add(url_path)

            # Datum finns i URL: .../titel-ort-2026-03-19/
            date_m = re.search(r'(202[5-9]-\d{2}-\d{2})', url_path)
            date_iso_val = date_m.group(1) if date_m else ""

            url = self.BASE_URL + url_path

            cats = self._guess_cats(title)
            events.append(self.event(
                title=title,
                date_iso=date_iso_val,
                url=url,
                description="",
                categories=cats,
            ))
        return events

    def _guess_cats(self, title):
        t = title.lower()
        if any(x in t for x in ["fågel", "uggla", "fisk", "däggdjur", "art"]): return ["biodiv"]
        if any(x in t for x in ["skog", "träd"]): return ["skog"]
        if any(x in t for x in ["vatten", "våtmark"]): return ["vatten"]
        if any(x in t for x in ["klimat"]): return ["klimat"]
        if any(x in t for x in ["odl", "mat"]): return ["mat"]
        return ["biodiv"]