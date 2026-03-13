c = open('scrapers/run_all.py', encoding='utf-8').read()

# Lägg till imports
old_import = 'from scrapers.underekarna import UnderekarnaScraper'
new_import = '''from scrapers.underekarna import UnderekarnaScraper
from scrapers.jordbruksverket import JordbruksverketScraper
from scrapers.svenskkolinlagring import SvenskKolinlagringScraper
from scrapers.sv_tradgard import SVTradgardScraper'''
c = c.replace(old_import, new_import)

# Lägg till instanser
old_inst = 'UnderekarnaScraper(),'
new_inst = '''UnderekarnaScraper(),
    JordbruksverketScraper(),
    SvenskKolinlagringScraper(),
    SVTradgardScraper(),'''
c = c.replace(old_inst, new_inst)

open('scrapers/run_all.py', 'w', encoding='utf-8').write(c)
print('Klar!')