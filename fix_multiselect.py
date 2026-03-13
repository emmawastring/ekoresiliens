c = open('index.html', encoding='utf-8').read()

# 1. Ändra activeCat och activeKBCat till arrays
c = c.replace(
    "let activeCat = 'all', activeTime = 'future', activeType = 'all', activeLang = 'all', activeKBType = 'all', activeKBCat = 'all', activeKBLang = 'all', activeKBSource = 'all';",
    "let activeCat = [], activeTime = 'future', activeType = 'all', activeLang = 'all', activeKBType = 'all', activeKBCat = [], activeKBLang = 'all', activeKBSource = 'all';"
)

# 2. Skriv om selectCat
old_selectCat = """function selectCat(el, groupId) {
  document.querySelectorAll('#' + groupId + ' .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  const v = el.dataset.cat;
  if (groupId === 'catChips')   { activeCat   = v; applyFilters(); }
  if (groupId === 'kbCatChips') { activeKBCat = v; renderKB(); }
}"""

new_selectCat = """function selectCat(el, groupId) {
  const v = el.dataset.cat;
  if (v === 'all') {
    // Nollställ – bara Alla aktiv
    document.querySelectorAll('#' + groupId + ' .chip').forEach(c => c.classList.remove('active'));
    el.classList.add('active');
    if (groupId === 'catChips')   { activeCat   = []; applyFilters(); }
    if (groupId === 'kbCatChips') { activeKBCat = []; renderKB(); }
  } else {
    // Avmarkera Alla
    document.querySelector('#' + groupId + ' .chip[data-cat="all"]').classList.remove('active');
    // Toggle detta chip
    el.classList.toggle('active');
    // Bygg ny array från aktiva chips
    const active = Array.from(document.querySelectorAll('#' + groupId + ' .chip.active')).map(c => c.dataset.cat).filter(c => c !== 'all');
    if (active.length === 0) {
      // Om inget är valt, aktivera Alla igen
      document.querySelector('#' + groupId + ' .chip[data-cat="all"]').classList.add('active');
    }
    if (groupId === 'catChips')   { activeCat   = active; applyFilters(); }
    if (groupId === 'kbCatChips') { activeKBCat = active; renderKB(); }
  }
}"""

c = c.replace(old_selectCat, new_selectCat)

# 3. Uppdatera filterlogiken för activeCat (events)
old_filter = "if (activeCat !== 'all') { const cats = w.categories || []; const titleDesc = (w.title + ' ' + (w.description || '')).toLowerCase(); const match = cats.includes(activeCat) || (activeCat === 'skogstradgard' && cats.includes('agroforestry')) || (activeCat === 'skog' && titleDesc.includes('forest')); if (!match) return false; }"

new_filter = "if (activeCat.length > 0) { const cats = w.categories || []; const titleDesc = (w.title + ' ' + (w.description || '')).toLowerCase(); const match = activeCat.some(ac => cats.includes(ac) || (ac === 'skogstradgard' && cats.includes('agroforestry')) || (ac === 'skog' && titleDesc.includes('forest'))); if (!match) return false; }"

c = c.replace(old_filter, new_filter)

# 4. Uppdatera filterlogiken för activeKBCat (KB)
old_kb_filter = "if (activeKBCat !== 'all' && !(r.cats || []).includes(activeKBCat)) return false;"
new_kb_filter = "if (activeKBCat.length > 0 && !activeKBCat.some(ac => (r.cats || []).includes(ac))) return false;"
c = c.replace(old_kb_filter, new_kb_filter)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')
print('selectCat omskriven:', 'function selectCat' in c)
print('activeCat array:', "activeCat = []" in c)