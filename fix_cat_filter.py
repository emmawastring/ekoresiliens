c = open('index.html', encoding='utf-8').read()

old = "if (activeCat !== 'all' && !(w.categories || []).includes(activeCat)) return false;"

new = "if (activeCat !== 'all') { const cats = w.categories || []; const match = cats.includes(activeCat) || (activeCat === 'skogstradgard' && cats.includes('agroforestry')); if (!match) return false; }"

c = c.replace(old, new)
open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!' if new in c else 'Ingen match!')