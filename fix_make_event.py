for f in ['scrapers/jordbruksverket.py', 'scrapers/svenskkolinlagring.py', 'scrapers/sv_tradgard.py']:
    c = open(f, encoding='utf-8').read()
    c = c.replace('self.make_event(', 'self.event(')
    open(f, 'w', encoding='utf-8').write(c)
    print(f'Fixade: {f}')