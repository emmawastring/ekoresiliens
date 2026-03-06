"""Generate/update knowledge_resources.json with YouTube videos and other resources."""

import json
from pathlib import Path

from scrapers.youtube import YouTubeScraper
from scrapers.movium_resources import fetch_movium_resources
from scrapers.unity_library import fetch_unity_library_resources
from scrapers.sciencedirect import fetch_sciencedirect_articles
from scrapers.naturvardsverket_kb import fetch_naturvardsverket_resources
from scrapers.boverket_kb import fetch_boverket_pbl_resources
from scrapers.cocity_kb import fetch_cocity_resources
from scrapers.millennium_assessment_kb import fetch_millennium_assessment_resources
from scrapers.slu_publications_kb import fetch_slu_publications
from scrapers.livsmedelsverket_kb import fetch_livsmedelsverket_resources
from scrapers.movium_news_kb import fetch_movium_news


# Channels to include: either YouTube ID or @handle/URL
# we include all five sources specified by user
CHANNELS = [
    ("UC77WnDnCntOzcQAIU_TPGnA", "Soil Food Web School"),
    ("https://www.youtube.com/@soilfoodwebschool", "Soil Food Web School"),
    ("https://www.youtube.com/@naturvardsverket", "Naturvårdsverket"),
    ("https://www.youtube.com/@borrabopermakulturjordliv", "Börra bo permakulturjordliv"),
    ("https://www.youtube.com/@grobladspermakultur1589", "Groblads Permakultur"),
    ("https://www.youtube.com/@agroforestry_paradigmshiftfilm", "Agroforestry Paradigm Shift Film"),
]


def run():
    data_path = Path(__file__).parent.parent / "data" / "knowledge_resources.json"
    if data_path.exists():
        kb = json.loads(data_path.read_text(encoding='utf-8'))
    else:
        kb = []

    # remove existing entries from these source names to avoid duplicates
    source_names = [name for _, name in CHANNELS] + [
        "SLU MOVIUM", "United Diversity Library", "ScienceDirect Open Access",
        "Naturvårdsverket", "Boverket PBL", "CoCity", "Millennium Ecosystem Assessment",
        "Sveriges lantbruksuniversitet", "Livsmedelsverket"
    ]
    kb = [r for r in kb if r.get('source_name') not in source_names]

    # Add YouTube videos
    for cid, name in CHANNELS:
        scraper = YouTubeScraper(cid, name)
        print(f"Fetching videos from {name}...")
        kb.extend(scraper.fetch())
    
    # Add MOVIUM resources
    print("Fetching MOVIUM resources...")
    kb.extend(fetch_movium_resources())
    
    # Add United Diversity Library resources
    print("Fetching United Diversity Library resources...")
    kb.extend(fetch_unity_library_resources())

    # Add ScienceDirect articles
    print("Fetching ScienceDirect articles...")
    kb.extend(fetch_sciencedirect_articles())

    # Add new KB scrapers
    print("Fetching Naturvårdsverket resources...")
    kb.extend(fetch_naturvardsverket_resources())

    print("Fetching Boverket PBL resources...")
    kb.extend(fetch_boverket_pbl_resources())

    print("Fetching CoCity resources...")
    kb.extend(fetch_cocity_resources())

    print("Fetching Millennium Assessment resources...")
    kb.extend(fetch_millennium_assessment_resources())

    print("Fetching SLU publications...")
    kb.extend(fetch_slu_publications())

    print("Fetching Livsmedelsverket publications...")
    kb.extend(fetch_livsmedelsverket_resources())

    print("Fetching MOVIUM news...")
    kb.extend(fetch_movium_news())

    # save back
    data_path.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote {len(kb)} knowledge resources total")


if __name__ == '__main__':
    run()
