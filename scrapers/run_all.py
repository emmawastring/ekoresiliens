"""
Ekoresiliens – scraper orchestrator
Kör alla scrapers och sparar resultatet till data/webinars.json
Körs av GitHub Actions dagligen, men kan också köras manuellt:
  python scrapers/run_all.py
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path

from scrapers.slu import SLUScraper
from scrapers.naturvardsverket import NaturvardsverketScraper
from scrapers.skogsstyrelsen import SkogsstyrelseScraper
from scrapers.hav import HaVScraper
from scrapers.smhi import SMHIScraper
from scrapers.sverigesradio import SVAScraper
from scrapers.agroforestry import AgroforestryScraper
from scrapers.permakultur import PermakulturScraper
from scrapers.region_vg import RegionVGScraper
from scrapers.movium import MoviumScraper
from scrapers.slu_urban import SLUUrbanScraper
from scrapers.boverket_webinar import BoverketWebinarScraper
from scrapers.boverket_kalender import BoverketKalenderScraper
from scrapers.omstallningsfonden import OmstallningsfondenScraper
from scrapers.nv_kalendarium import NVKalendariumScraper
from scrapers.aktuell_hallbarhet import AktuellHallbarhetScraper
from scrapers.slu_play import SLUPlayScraper

SCRAPERS = [
    SLUScraper(),
    NaturvardsverketScraper(),
    SkogsstyrelseScraper(),
    HaVScraper(),
    SMHIScraper(),
    SVAScraper(),
    AgroforestryScraper(),
    PermakulturScraper(),
    RegionVGScraper(),
    MoviumScraper(),
    SLUUrbanScraper(),
    BoverketWebinarScraper(),
    BoverketKalenderScraper(),
    OmstallningsfondenScraper(),
    NVKalendariumScraper(),
    AktuellHallbarhetScraper(),
    SLUPlayScraper(),
]

OUTPUT_PATH = Path(__file__).parent.parent / "data" / "webinars.json"


def run():
    all_events = []
    errors = []

    for scraper in SCRAPERS:
        try:
            print(f"  → Kör {scraper.name}...")
            events = scraper.fetch()
            print(f"    ✓ Hittade {len(events)} evenemang")
            all_events.extend(events)
        except Exception as e:
            msg = f"{scraper.name}: {e}"
            errors.append(msg)
            print(f"    ✗ Fel: {e}")

    # Sortera på datum, ta bort förflutna
    now = datetime.now(timezone.utc)
    upcoming = [e for e in all_events if e.get("date_iso") and e["date_iso"] >= now.isoformat()[:10]]
    upcoming.sort(key=lambda x: x["date_iso"])

    # Deduplicera på titel+datum
    seen = set()
    unique = []
    for e in upcoming:
        key = (e["title"].lower().strip(), e["date_iso"])
        if key not in seen:
            seen.add(key)
            unique.append(e)

    output = {
        "updated": datetime.now(timezone.utc).isoformat(),
        "count": len(unique),
        "errors": errors,
        "events": unique,
    }

    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✅ Sparade {len(unique)} unika evenemang till {OUTPUT_PATH}")
    if errors:
        print(f"⚠️  {len(errors)} scrapers misslyckades: {', '.join(errors)}")


if __name__ == "__main__":
    print("🌿 Ekoresiliens – hämtar evenemang...\n")
    run()
