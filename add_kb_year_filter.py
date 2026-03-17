c = open('index.html', encoding='utf-8').read()

# 1. Lägg till år i kb-footer
old_footer = '''      <div class="kb-footer">
        <span class="kb-source-small">${r.source}</span>
        <span class="kb-link-hint">Öppna →</span>
      </div>'''
new_footer = '''      <div class="kb-footer">
        <span class="kb-source-small">${r.source}</span>
        <span class="kb-source-small" style="color:var(--bark)">${r.year ? r.year : ''}</span>
        <span class="kb-link-hint">Öppna →</span>
      </div>'''
c = c.replace(old_footer, new_footer)

# 2. Lägg till activeKBYear i variabeldeklarationen
c = c.replace(
    "activeKBSource = 'all';",
    "activeKBSource = 'all', activeKBYear = 'all';"
)

# 3. Lägg till årsfilter i renderKB
old_filter = "    if (activeSources.length > 0 && !activeSources.includes(r.source_name || r.source)) return false;"
new_filter = """    if (activeSources.length > 0 && !activeSources.includes(r.source_name || r.source)) return false;
    if (activeKBYear !== 'all') {
      const yr = r.year || 0;
      const now = new Date().getFullYear();
      if (activeKBYear === 'new'  && yr < now - 1) return false;
      if (activeKBYear === '3yr'  && yr < now - 3) return false;
      if (activeKBYear === '5yr'  && yr < now - 5) return false;
      if (activeKBYear === 'old'  && yr >= now - 5) return false;
    }"""
c = c.replace(old_filter, new_filter)

# 4. Hitta var KB-filterpanelen slutar (efter kbLangChips) och lägg till årsfilter
# Hitta lämplig plats – efter språkfilter-gruppen i KB
old_lang_group = '''            <div class="filter-group-label" onclick="toggleFilterGroup(this)">Språk</div>'''
# Lägg till årsfilter-grupp FÖRE språkgruppen
new_year_group = '''            <div class="filter-group-label" onclick="toggleFilterGroup(this)">Publiceringsår</div>
              <div class="filter-group-body">
                <div class="chip-group" id="kbYearChips">
                  <div class="chip active" data-year="all"  onclick="selectKBYear(this)">Alla år</div>
                  <div class="chip"        data-year="new"  onclick="selectKBYear(this)">Senaste 2 år</div>
                  <div class="chip"        data-year="3yr"  onclick="selectKBYear(this)">Senaste 3 år</div>
                  <div class="chip"        data-year="5yr"  onclick="selectKBYear(this)">Senaste 5 år</div>
                  <div class="chip"        data-year="old"  onclick="selectKBYear(this)">Äldre</div>
                </div>
              </div>
            </div>
            <div class="filter-group">
            <div class="filter-group-label" onclick="toggleFilterGroup(this)">Språk</div>'''
c = c.replace(old_lang_group, new_year_group)

# 5. Lägg till selectKBYear-funktion efter selectLang
old_func = "function selectLang(el, groupId) {"
new_func = """function selectKBYear(el) {
  document.querySelectorAll('#kbYearChips .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  activeKBYear = el.dataset.year;
  renderKB();
}
function selectLang(el, groupId) {"""
c = c.replace(old_func, new_func)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')