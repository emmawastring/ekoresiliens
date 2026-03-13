c = open('index.html', encoding='utf-8').read()

old = "if (activeKBCat  !== 'all' && !(r.cats || []).includes(activeKBCat)) return false;"
new = "if (activeKBCat.length > 0 && !activeKBCat.some(ac => (r.cats || []).includes(ac))) return false;"

if old in c:
    c = c.replace(old, new)
    open('index.html', 'w', encoding='utf-8').write(c)
    print('Fixat!')
else:
    print('Hittade inte strängen, söker...')
    idx = c.find('activeKBCat')
    print(c[idx-50:idx+150])