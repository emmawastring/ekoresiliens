c = open('scrapers/run_all.py', encoding='utf-8').read()
old = 'LansstyrelseScraper("Skåne",           "https://www.lansstyrelsen.se/skane/om-oss/kalender/kalenderhandelser---skane/")'
new = 'LansstyrelseScraper("Skåne",           "https://www.lansstyrelsen.se/skane/om-oss/kalender/")'
c = c.replace(old, new)
open('scrapers/run_all.py', 'w', encoding='utf-8').write(c)
print('Klar!' if new in c else 'Ingen match!')