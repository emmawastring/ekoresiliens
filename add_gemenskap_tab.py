c = open('index.html', encoding='utf-8').read()

# 1. Lägg till tab-knapp
old_tabs = '    <button class="tab-btn" onclick="switchTab(\'kunskapsbank\')" id="tab-kunskapsbank">Kunskapsbank</button>'
new_tabs = '''    <button class="tab-btn" onclick="switchTab('kunskapsbank')" id="tab-kunskapsbank">Kunskapsbank</button>
    <button class="tab-btn" onclick="switchTab('gemenskap')" id="tab-gemenskap">Gemenskap</button>'''
c = c.replace(old_tabs, new_tabs)

# 2. Lägg till panel efter KB-panelens stängande </div> (rad 521)
old_panel_end = '</div>\n<footer>'
new_panel = '''</div>

<!-- ════════════════════════════════════ -->
<!-- TAB 3 – GEMENSKAP                   -->
<!-- ════════════════════════════════════ -->
<div class="tab-panel" id="panel-gemenskap">
  <div class="main-wrap">
    <aside>
      <div class="filter-card">
        <div class="filter-title">🔍 Sök &amp; Filtrera</div>
        <input class="search-box" type="text" placeholder="Sök förening, nätverk..." id="gemSearch" oninput="renderGem()">
        <div id="gemVisibleCount" style="font-size:.8rem;color:var(--bark);margin:.4rem 0">–</div>
        <div class="filter-group">
          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Typ</div>
          <div class="filter-group-body">
            <div class="chip-group" id="gemTypeChips">
              <div class="chip active" data-gemtype="all"        onclick="selectGemType(this)">Alla</div>
              <div class="chip"        data-gemtype="forening"   onclick="selectGemType(this)">Förening</div>
              <div class="chip"        data-gemtype="nätverk"    onclick="selectGemType(this)">Nätverk</div>
              <div class="chip"        data-gemtype="kooperativ" onclick="selectGemType(this)">Kooperativ</div>
              <div class="chip"        data-gemtype="community"  onclick="selectGemType(this)">Community</div>
              <div class="chip"        data-gemtype="rörelse"    onclick="selectGemType(this)">Rörelse</div>
            </div>
          </div>
        </div>
        <div class="filter-group">
          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Kategori</div>
          <div class="filter-group-body">
            <div class="chip-group" id="gemCatChips">
              <div class="chip active" data-cat="all"         onclick="selectCat(this,'gemCatChips')">Alla</div>
              <div class="chip"        data-cat="omstallning" onclick="selectCat(this,'gemCatChips')">Omställning</div>
              <div class="chip"        data-cat="mat"         onclick="selectCat(this,'gemCatChips')">Mat & Odling</div>
              <div class="chip"        data-cat="skog"        onclick="selectCat(this,'gemCatChips')">Skog</div>
              <div class="chip"        data-cat="biodiv"      onclick="selectCat(this,'gemCatChips')">Biologisk mångfald</div>
              <div class="chip"        data-cat="klimat"      onclick="selectCat(this,'gemCatChips')">Klimat</div>
              <div class="chip"        data-cat="beredskap"   onclick="selectCat(this,'gemCatChips')">Beredskap</div>
              <div class="chip"        data-cat="skogstradgard" onclick="selectCat(this,'gemCatChips')">Skogsträdgård</div>
            </div>
          </div>
        </div>
      </div>
    </aside>
    <main>
      <div id="gemContent" class="kb-grid"></div>
      <div id="gemEmpty" style="display:none;text-align:center;padding:3rem">
        <div class="icon">🤝</div>
        <p>Inga träffar</p>
      </div>
    </main>
  </div>
</div>
<footer>'''
c = c.replace('</div>\n<footer>', new_panel, 1)

# 3. Lägg till gemenskapsdata och renderGem-funktion i JS
old_init = 'async function init() {'
new_js = '''// ═══════════════════════════════════════════
// GEMENSKAP
// ═══════════════════════════════════════════
let allGem = [];
let activeGemType = 'all', activeGemCat = [];

async function loadGem() {
  try {
    const r = await fetch('data/gemenskap.json');
    const json = await r.json();
    allGem = json.orgs || [];
    renderGem();
  } catch(e) { console.warn('gemenskap.json saknas', e); }
}

function selectGemType(el) {
  document.querySelectorAll('#gemTypeChips .chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  activeGemType = el.dataset.gemtype;
  renderGem();
}

function renderGem() {
  const q = (document.getElementById('gemSearch')?.value || '').toLowerCase();
  let f = allGem.filter(g => {
    if (activeGemType !== 'all' && g.type !== activeGemType) return false;
    if (activeGemCat.length > 0 && !activeGemCat.some(ac => (g.cats||[]).includes(ac))) return false;
    if (q && !g.name.toLowerCase().includes(q) && !(g.desc||'').toLowerCase().includes(q)) return false;
    return true;
  });
  const cont  = document.getElementById('gemContent');
  const empty = document.getElementById('gemEmpty');
  const cnt   = document.getElementById('gemVisibleCount');
  if (cnt) cnt.textContent = f.length + ' organisationer';
  if (!f.length) { cont.innerHTML = ''; empty.style.display = 'block'; return; }
  empty.style.display = 'none';
  cont.innerHTML = f.map(g => `
    <a class="kb-card" href="${g.url}" target="_blank" rel="noopener noreferrer">
      <div style="height:80px;background:linear-gradient(135deg,#f5f0e8 0%,#faf7f2 100%);display:flex;align-items:center;justify-content:center;padding:0.8rem;border-bottom:1px solid var(--mist);">
        <img src="${getFaviconUrl(g.url)}" alt="" style="max-width:50px;max-height:50px;object-fit:contain;" onerror="this.style.display='none'">
      </div>
      <div class="kb-card-top">
        <span class="kb-icon">${g.icon || '🤝'}</span>
        <span class="kb-type-badge" style="background:#e8f0e8;color:#2d6a2d;border:1px solid #b5d0b5">${g.type || 'förening'}</span>
      </div>
      <div class="kb-title">${g.name}</div>
      <div class="kb-desc">${g.desc || ''}</div>
      <div class="kb-tags">${(g.cats||[]).map(t=>`<span class="tag cat-${t}">${tl(t)}</span>`).join('')}</div>
      <div class="kb-footer">
        <span class="kb-source-small">${g.location || ''}</span>
        <span class="kb-link-hint">Besök →</span>
      </div>
    </a>`).join('');
}

// Koppla gemCatChips till activeGemCat
const _origSelectCat = selectCat;

async function init() {'''
c = c.replace('async function init() {', new_js)

# 4. Lägg till loadGem() i init
old_init2 = '  await Promise.all([loadWebinars(), loadKB()]);'
new_init2 = '  await Promise.all([loadWebinars(), loadKB(), loadGem()]);'
c = c.replace(old_init2, new_init2)

# 5. Koppla selectCat för gemCatChips
old_selectcat_kb = "    if (groupId === 'kbCatChips') { activeKBCat = []; renderKB(); }"
new_selectcat_kb = """    if (groupId === 'kbCatChips') { activeKBCat = []; renderKB(); }
    if (groupId === 'gemCatChips') { activeGemCat = []; renderGem(); }"""
c = c.replace(old_selectcat_kb, new_selectcat_kb)

old_selectcat_kb2 = "    if (groupId === 'kbCatChips') { activeKBCat = active; renderKB(); }"
new_selectcat_kb2 = """    if (groupId === 'kbCatChips') { activeKBCat = active; renderKB(); }
    if (groupId === 'gemCatChips') { activeGemCat = active; renderGem(); }"""
c = c.replace(old_selectcat_kb2, new_selectcat_kb2)

open('index.html', 'w', encoding='utf-8').write(c)
print('index.html uppdaterad!')