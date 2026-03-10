import os
import re

scrapers_dir = 'scrapers'
updated = []

for fname in os.listdir(scrapers_dir):
    if not fname.endswith('.py') or fname.startswith('__'):
        continue
    fpath = os.path.join(scrapers_dir, fname)
    c = open(fpath, encoding='utf-8').read()
    if '"samhalle"' in c or "'samhalle'" in c:
        c = c.replace('"samhalle"', '"omstallning"')
        c = c.replace("'samhalle'", "'omstallning'")
        open(fpath, 'w', encoding='utf-8').write(c)
        updated.append(fname)

print(f'Uppdaterade {len(updated)} filer:')
for f in updated:
    print(f'  {f}')