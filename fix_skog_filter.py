c = open('index.html', encoding='utf-8').read()

# Ta bort dubbletten (den med #1b5e20)
c = c.replace(
    '\n              <div class="chip" data-cat="skogstradgard" onclick="selectCat(this,\'catChips\')"><span class="chip-dot" style="background:#1b5e20"></span>Skogsträdgård</div>',
    ''
)

# Lägg till "forest" i skog-filtret i applyFilters
c = c.replace(
    "if (activeCat !== 'all') { const cats = w.categories || []; const match = cats.includes(activeCat) || (activeCat === 'skogstradgard' && cats.includes('agroforestry')); if (!match) return false; }",
    "if (activeCat !== 'all') { const cats = w.categories || []; const titleDesc = (w.title + ' ' + (w.description || '')).toLowerCase(); const match = cats.includes(activeCat) || (activeCat === 'skogstradgard' && cats.includes('agroforestry')) || (activeCat === 'skog' && titleDesc.includes('forest')); if (!match) return false; }"
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')