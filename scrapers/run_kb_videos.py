"""Generate/update knowledge_resources.json with YouTube videos."""

import json
from pathlib import Path

from scrapers.youtube import YouTubeScraper

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
    source_names = [name for _, name in CHANNELS]
    kb = [r for r in kb if r.get('source_name') not in source_names]

    for cid, name in CHANNELS:
        scraper = YouTubeScraper(cid, name)
        print(f"Fetching videos from {name}...")
        kb.extend(scraper.fetch())

    # save back
    data_path.write_text(json.dumps(kb, ensure_ascii=False, indent=2), encoding='utf-8')
    print(f"Wrote {len(kb)} knowledge resources (including YouTube videos)")


if __name__ == '__main__':
    run()
