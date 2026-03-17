c = open('scrapers/run_all.py', encoding='utf-8').read()
old = 'from scrapers.sv_tradgard import SVTradgardScraper'
new = '''from scrapers.sv_tradgard import SVTradgardScraper
from scrapers.landsbygdsnatverket import LandsbygdsnatverketScraper'''
c = c.replace(old, new)
old2 = 'SVTradgardScraper(),'
new2 = '''SVTradgardScraper(),
    LandsbygdsnatverketScraper(),'''
c = c.replace(old2, new2)
open('scrapers/run_all.py', 'w', encoding='utf-8').write(c)
print('Klar!')