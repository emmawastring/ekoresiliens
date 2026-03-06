"""
Ekoresiliens – scraper orchestrator
Kör alla scrapers och sparar resultatet till data/webinars.json
Körs av GitHub Actions dagligen, men kan också köras manuellt:
  python -m scrapers.run_all
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

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
from scrapers.treesforme import TreesForMeScraper
from scrapers.svenskt_vatten import SvensktVattenScraper
from scrapers.klimat2030 import Klimat2030Scraper
from scrapers.business_biodiversity import BusinessBiodiversityScraper
from scrapers.lansstyrelsen import LansstyrelseScraper
from scrapers.energimyndigheten import EnergimyndighetenScraper
from scrapers.ekocentrum import EkocentrumScraper
from scrapers.lrf import LRFScraper
from scrapers.klimatriksdagen import KlimatriksdagenScraper
from scrapers.ekologigruppen import EkologigruppenScraper

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
    TreesForMeScraper(),
    SvensktVattenScraper(),
    Klimat2030Scraper(),
    BusinessBiodiversityScraper(),
    LansstyrelseScraper("Skåne",           "https://www.lansstyrelsen.se/skane/om-oss/kalender/kalenderhandelser---skane/"),
    LansstyrelseScraper("Västra Götaland", "https://www.lansstyrelsen.se/vastra-gotaland/om-oss/kalender.html"),
    LansstyrelseScraper("Blekinge",        "https://www.lansstyrelsen.se/blekinge/om-oss/kalender.html"),
    LansstyrelseScraper("Dalarna",         "https://www.lansstyrelsen.se/dalarna/om-oss/kalender.html"),
    LansstyrelseScraper("Gotland",         "https://www.lansstyrelsen.se/gotland/om-oss/kalender.html"),
    LansstyrelseScraper("Gävleborg",       "https://www.lansstyrelsen.se/gavleborg/om-oss/kalender.html"),
    LansstyrelseScraper("Halland",         "https://www.lansstyrelsen.se/halland/om-oss/kalender.html"),
    LansstyrelseScraper("Jämtland",        "https://www.lansstyrelsen.se/jamtland/om-oss/kalender.html"),
    LansstyrelseScraper("Jönköping",       "https://www.lansstyrelsen.se/jonkoping/om-oss/kalender.html"),
    LansstyrelseScraper("Kalmar",          "https://www.lansstyrelsen.se/kalmar/om-oss/kalender.html"),
    LansstyrelseScraper("Kronoberg",       "https://www.lansstyrelsen.se/kronoberg/om-oss/kalender.html"),
    LansstyrelseScraper("Norrbotten",      "https://www.lansstyrelsen.se/norrbotten/om-oss/kalender.html"),
    LansstyrelseScraper("Stockholm",       "https://www.lansstyrelsen.se/stockholm/om-oss/kalender.html"),
    LansstyrelseScraper("Södermanland",    "https://www.lansstyrelsen.se/sodermanland/om-oss/kalender.html"),
    LansstyrelseScraper("Uppsala",         "https://www.lansstyrelsen.se/uppsala/om-oss/kalender.html"),
    LansstyrelseScraper("Värmland",        "https://www.lansstyrelsen.se/varmland/om-oss/kalender.html"),
    LansstyrelseScraper("Västmanland",     "https://www.lansstyrelsen.se/vastmanland/om-oss/kalender.html"),
    LansstyrelseScraper("Örebro",          "https://www.lansstyrelsen.se/orebro/om-oss/kalender.html"),
    LansstyrelseScraper("Östergötland",    "https://www.lansstyrelsen.se/ostergotland/om-oss/kalender.html"),
    EnergimyndighetenScraper(),
    EkocentrumScraper(),
    LRFScraper(),
    KlimatriksdagenScraper(),
    EkologigruppenScraper(),
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

    # INGEN datumfiltrering här – frontenden visar bara event från idag och framåt.
    all_events.sort(key=lambda x: x.get("date_iso") or "9999-99-99")

    seen = set()
    unique = []
    for e in all_events:
        key = (e["title"].lower().strip(), e.get("date_iso", ""))
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
        print(f"⚠️  {len(errors)} scrapers misslyckades")


if __name__ == "__main__":
    print("🌿 Ekoresiliens – hämtar evenemang...\n")
    run()
