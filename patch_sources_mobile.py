import re

content = open('index.html', encoding='utf-8').read()
original_len = len(content)
changes = 0

# ══════════════════════════════════════════
# 1. KOLLAPSBAR KÄLLLISTA – CSS
# ══════════════════════════════════════════
source_css = """
/* Kollapsbar källlista */
.source-toggle-row{display:flex;gap:6px;align-items:center;flex-wrap:wrap;margin-bottom:.3rem;}
.btn-source-toggle{background:var(--cream);border:1.5px solid var(--mist);color:var(--charcoal);
  font-family:'DM Sans',sans-serif;font-size:.76rem;padding:4px 10px;border-radius:20px;
  cursor:pointer;display:flex;align-items:center;gap:4px;transition:border-color .15s;}
.btn-source-toggle:hover{border-color:var(--fern);color:var(--fern);}
.btn-source-toggle.active-all{background:var(--fern);color:#fff;border-color:var(--fern);}
.source-list-collapsible{display:none;margin-top:.5rem;}
.source-list-collapsible.open{display:flex;flex-direction:column;gap:5px;}

/* ══ MOBILANPASSNING ══ */
@media(max-width:600px){
  .hero{padding:1.5rem 1rem 1.5rem;}
  .hero h1{font-size:1.4rem;}
  .hero p{font-size:.85rem;}
  .stats-row{gap:.7rem;}
  .stat-link{padding:.5rem .7rem;}
  .stat-link .stat-num{font-size:1.2rem;}
  .main-wrap{flex-direction:column;padding:.8rem;}
  aside{width:100%;position:static;}
  .filter-card{padding:1rem;}
  .cards-grid{grid-template-columns:1fr;}
  .kb-grid{grid-template-columns:1fr;}
  .toolbar{flex-direction:column;align-items:flex-start;}
  .logo{font-size:1.15rem;}
  .btn-primary{padding:7px 13px;font-size:.78rem;}
  .updated-info{display:none;}
  .panel-filter-bar{padding:.5rem .8rem;gap:.5rem;flex-wrap:wrap;}
  .panel-filter-bar .filter-label{width:100%;}
  .chip{font-size:.72rem;padding:3px 8px;}
  .card-body{padding:.8rem;}
  .card-title{font-size:.92rem;}
  .card-desc{display:none;}
  a.card{border-radius:12px;}
  footer{padding:1rem;font-size:.72rem;}
  .creator{gap:.4rem;}
}
@media(max-width:400px){
  .hero h1{font-size:1.2rem;}
  .stats-row{flex-direction:column;align-items:center;}
  .stat-link{width:80%;max-width:200px;}
}
"""

# Inject before closing </style>
if '</style>' in content:
    content = content.replace('</style>', source_css + '</style>', 1)
    changes += 1
    print("1. CSS tillagd (kollapsbar källlista + mobil)")

# ══════════════════════════════════════════
# 2. KÄLLFILTER HTML – events-panelen
# ══════════════════════════════════════════
old_source_filter = '''        <div class="filter-group">
          <div class="filter-group-label">K\u00e4lla</div>
          <div class="source-list" id="sourceList">
            <!-- Genereras dynamiskt fr\u00e5n data -->
          </div>
        </div>
      </div>
    </aside>

    <main>'''

new_source_filter = '''        <div class="filter-group">
          <div class="filter-group-label">K\u00e4lla</div>
          <div class="source-toggle-row">
            <button class="btn-source-toggle active-all" id="srcAllBtn" onclick="selectAllSources()">Alla</button>
            <button class="btn-source-toggle" id="srcToggleBtn" onclick="toggleSourceList()">V\u00e4lj k\u00e4llor \u25be</button>
          </div>
          <div class="source-list-collapsible" id="sourceListWrap">
            <div class="source-list" id="sourceList"></div>
          </div>
        </div>
      </div>
    </aside>

    <main>'''

if old_source_filter in content:
    content = content.replace(old_source_filter, new_source_filter, 1)
    changes += 1
    print("2. Källfilter HTML (events) uppdaterad")
else:
    print("2. VARNING: Källfilter HTML (events) hittades ej")

# ══════════════════════════════════════════
# 3. KÄLLFILTER HTML – KB-panelen
# ══════════════════════════════════════════
old_kb_source = '''        <div class="filter-group">
          <div class="filter-group-label">K\u00e4lla</div>
          <div class="source-list" id="kbSourceList">
            <!-- Genereras dynamiskt fr\u00e5n data -->
          </div>
        </div>'''

new_kb_source = '''        <div class="filter-group">
          <div class="filter-group-label">K\u00e4lla</div>
          <div class="source-toggle-row">
            <button class="btn-source-toggle active-all" id="kbSrcAllBtn" onclick="selectAllKBSources()">Alla</button>
            <button class="btn-source-toggle" id="kbSrcToggleBtn" onclick="toggleKBSourceList()">V\u00e4lj k\u00e4llor \u25be</button>
          </div>
          <div class="source-list-collapsible" id="kbSourceListWrap">
            <div class="source-list" id="kbSourceList"></div>
          </div>
        </div>'''

if old_kb_source in content:
    content = content.replace(old_kb_source, new_kb_source, 1)
    changes += 1
    print("3. Källfilter HTML (KB) uppdaterad")
else:
    print("3. VARNING: Källfilter HTML (KB) hittades ej")

# ══════════════════════════════════════════
# 4. JS – toggle-funktioner + uppdatera buildSourceList
# ══════════════════════════════════════════
toggle_js = """
// ═══════════════════════════════════════════
// KÄLLLISTA TOGGLE
// ═══════════════════════════════════════════
function toggleSourceList() {
  var wrap = document.getElementById('sourceListWrap');
  var btn  = document.getElementById('srcToggleBtn');
  var all  = document.getElementById('srcAllBtn');
  var open = wrap.classList.toggle('open');
  btn.textContent = open ? 'D\u00f6lj k\u00e4llor \u25b4' : 'V\u00e4lj k\u00e4llor \u25be';
  all.classList.toggle('active-all', !open);
}

function selectAllSources() {
  // St\u00e4ng listan och markera alla
  var wrap = document.getElementById('sourceListWrap');
  var btn  = document.getElementById('srcToggleBtn');
  var all  = document.getElementById('srcAllBtn');
  wrap.classList.remove('open');
  btn.textContent = 'V\u00e4lj k\u00e4llor \u25be';
  all.classList.add('active-all');
  document.querySelectorAll('#sourceList input[type="checkbox"]').forEach(c => c.checked = true);
  applyFilters();
}

function toggleKBSourceList() {
  var wrap = document.getElementById('kbSourceListWrap');
  var btn  = document.getElementById('kbSrcToggleBtn');
  var all  = document.getElementById('kbSrcAllBtn');
  var open = wrap.classList.toggle('open');
  btn.textContent = open ? 'D\u00f6lj k\u00e4llor \u25b4' : 'V\u00e4lj k\u00e4llor \u25be';
  all.classList.toggle('active-all', !open);
}

function selectAllKBSources() {
  var wrap = document.getElementById('kbSourceListWrap');
  var btn  = document.getElementById('kbSrcToggleBtn');
  var all  = document.getElementById('kbSrcAllBtn');
  wrap.classList.remove('open');
  btn.textContent = 'V\u00e4lj k\u00e4llor \u25be';
  all.classList.add('active-all');
  document.querySelectorAll('#kbSourceList input[type="checkbox"]').forEach(c => c.checked = true);
  renderKB();
}

"""

# Inject before the DATA comment block
marker = "// \u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n// DATA"
if marker in content:
    content = content.replace(marker, toggle_js + marker, 1)
    changes += 1
    print("4. Toggle-JS tillagd")
else:
    # fallback – inject before init()
    content = content.replace('init();\n</script>', toggle_js + 'init();\n</script>', 1)
    changes += 1
    print("4. Toggle-JS tillagd (fallback)")

open('index.html', 'w', encoding='utf-8').write(content)
print(f"\nKlar! {changes} \u00e4ndringar, {original_len} -> {len(content)} tecken")