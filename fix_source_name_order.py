for fpath in ['scrapers/holma.py', 'scrapers/hutskane.py', 'scrapers/omstallningskanalen.py']:
    c = open(fpath, encoding='utf-8').read()
    # Ta bort den felaktigt insatta raden
    c = c.replace('    name = SOURCE_NAME\n    source_id = ', '    source_id = ')
    # Hitta SOURCE_NAME = "..." och lägg till name = SOURCE_NAME efter
    import re
    def add_name(m):
        return m.group(0) + '\n    name = SOURCE_NAME'
    c = re.sub(r'    SOURCE_NAME = "[^"]*"', add_name, c, count=1)
    open(fpath, 'w', encoding='utf-8').write(c)
    print(f'Fixade: {fpath}')
    # Visa de relevanta raderna
    for i, line in enumerate(c.splitlines()):
        if 'SOURCE_NAME' in line or 'name =' in line or 'source_id' in line:
            print(f'  {i+1}: {line}')