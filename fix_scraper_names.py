import re

# 1. Lägg till name= i holma, hutskane, omstallningskanalen
fixes = {
    'scrapers/holma.py': ('SOURCE_NAME = ', 'name = SOURCE_NAME\n    source_id = "holma"\n    SOURCE_NAME = '),
    'scrapers/hutskane.py': ('SOURCE_NAME = ', 'name = SOURCE_NAME\n    source_id = "hutskane"\n    SOURCE_NAME = '),
    'scrapers/omstallningskanalen.py': ('SOURCE_NAME = ', 'name = SOURCE_NAME\n    source_id = "omstallningskanalen"\n    SOURCE_NAME = '),
}

for fpath, (old_snippet, new_snippet) in fixes.items():
    c = open(fpath, encoding='utf-8').read()
    # Hitta SOURCE_NAME inne i klassen
    if 'name = SOURCE_NAME' not in c:
        c = c.replace('    ' + old_snippet, '    ' + new_snippet, 1)
        open(fpath, 'w', encoding='utf-8').write(c)
        print(f'Fixade: {fpath}')
    else:
        print(f'Redan fixad: {fpath}')

# 2. Ta bort dubbel NaturvardsverketScraper i run_all.py
c = open('scrapers/run_all.py', encoding='utf-8').read()

# Ta bort den tidiga importen (rad 16)
lines = c.splitlines()
seen_nv_import = False
new_lines = []
for line in lines:
    if 'from scrapers.naturvardsverket import NaturvardsverketScraper' in line:
        if seen_nv_import:
            print('Tog bort dubbel NV-import')
            continue
        seen_nv_import = True
    new_lines.append(line)
c = '\n'.join(new_lines)

# Ta bort den tidiga NaturvardsverketScraper()-instansen (rad 51)
seen_nv_instance = False
new_lines2 = []
for line in c.splitlines():
    if line.strip() == 'NaturvardsverketScraper(),':
        if seen_nv_instance:
            print('Tog bort dubbel NV-instans')
            continue
        seen_nv_instance = True
    new_lines2.append(line)
c = '\n'.join(new_lines2)

open('scrapers/run_all.py', 'w', encoding='utf-8').write(c)
print('run_all.py klar!')