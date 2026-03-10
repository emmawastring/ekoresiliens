c = open('scrapers/run_all.py', encoding='utf-8').read()
c = c.replace(
    'from scrapers.holma import HolmaScraper',
    'from scrapers.underekarna import UnderekarnaScraper\nfrom scrapers.naturvardsverket import NaturvardsverketScraper\nfrom scrapers.holma import HolmaScraper'
).replace(
    '    HolmaScraper(),',
    '    UnderekarnaScraper(),\n    NaturvardsverketScraper(),\n    HolmaScraper(),'
)
open('scrapers/run_all.py', 'w', encoding='utf-8').write(c)
print('Klar!')