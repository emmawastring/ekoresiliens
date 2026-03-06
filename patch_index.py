#!/usr/bin/env python3
"""
Applicera visuella ändringar på index.html:
1. Ta bort "Källor" och "Alltid kostnadsfritt" rutor
2. Gör "Evenemang" och "Kunskapsresurser" klickbara
3. Bakgrundsbild från geekyfarmers.com med grön fallback
"""

import sys

src = "index.html"
try:
    content = open(src, encoding="utf-8").read()
except FileNotFoundError:
    print(f"Hittade inte {src} – kör skriptet från projektets rotkatalog")
    sys.exit(1)

original = content
changes = 0

# ── 1. Lägg till background-size/position i .hero CSS ──
old = ".hero{background:var(--moss);background-image:radial-gradient(ellipse at 20% 50%,rgba(88,129,87,.6) 0%,transparent 60%),radial-gradient(ellipse at 80% 20%,rgba(163,184,153,.3) 0%,transparent 50%);padding:3rem 2rem 2.5rem;text-align:center;position:relative;overflow:hidden;}"
new = ".hero{background:var(--moss);background-image:radial-gradient(ellipse at 20% 50%,rgba(88,129,87,.6) 0%,transparent 60%),radial-gradient(ellipse at 80% 20%,rgba(163,184,153,.3) 0%,transparent 50%);padding:3rem 2rem 2.5rem;text-align:center;position:relative;overflow:hidden;background-size:cover;background-position:center;}"
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ Hero CSS: background-size/position tillagd")
else:
    print("⚠ Hero CSS: hittades ej – kontrollera manuellt")

# ── 2. Lägg till .stat-link CSS efter .stat-label ──
old = ".stat-label{font-size:.72rem;color:var(--mist);opacity:.8;}"
new = """.stat-label{font-size:.72rem;color:var(--mist);opacity:.8;}
.stat-link{background:rgba(255,255,255,.08);border:1px solid rgba(163,184,153,.3);border-radius:12px;padding:.6rem 1rem;text-align:center;cursor:pointer;transition:background .2s,border-color .2s;text-decoration:none;display:block;}
.stat-link:hover{background:rgba(255,255,255,.18);border-color:rgba(163,184,153,.8);}
.stat-link .stat-num{font-family:'Playfair Display',serif;font-size:1.5rem;color:var(--sage);display:block;}
.stat-link .stat-label{font-size:.72rem;color:var(--mist);opacity:.8;}"""
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ .stat-link CSS tillagd")
else:
    print("⚠ .stat-label CSS: hittades ej")

# ── 3. Byt ut stats-row HTML ──
old = """  <div class="stats-row">
    <div class="stat"><span class="stat-num" id="statWebinars">—</span><span class="stat-label">Kommande evenemang</span></div>
    <div class="stat"><span class="stat-num" id="statSources">—</span><span class="stat-label">Källor</span></div>
    <div class="stat"><span class="stat-num" id="statKB">—</span><span class="stat-label">Kunskapsresurser</span></div>
    <div class="stat"><span class="stat-num">Gratis</span><span class="stat-label">Alltid kostnadsfritt</span></div>
  </div>"""
new = """  <div class="stats-row">
    <a class="stat-link" onclick="switchTab('webbinarier');return false;" href="#">
      <span class="stat-num" id="statWebinars">—</span>
      <span class="stat-label">Kommande evenemang</span>
    </a>
    <a class="stat-link" onclick="switchTab('kunskapsbank');return false;" href="#">
      <span class="stat-num" id="statKB">—</span>
      <span class="stat-label">Kunskapsresurser</span>
    </a>
  </div>"""
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ Stats-rutor: Källor och Gratis borttagna, rutor klickbara")
else:
    print("⚠ stats-row HTML: hittades ej – kontrollera manuellt")

# ── 4. Ta bort statSources-raden i JS ──
old = """    document.getElementById('statWebinars').textContent = allWebinars.length;
    document.getElementById('statSources').textContent  = sourcesInData.length || '—';"""
new = "    document.getElementById('statWebinars').textContent = allWebinars.length;"
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ statSources JS-rad borttagen")
else:
    print("⚠ statSources JS: hittades ej")

# ── 5. Lägg till hero-bakgrundsbild JS precis före </script> ──
hero_js = """
// Ladda bakgrundsbild från geekyfarmers.com – faller tillbaka på grön om bilden misslyckas
(function() {
  // Prova flera möjliga bilder på geekyfarmers.com
  var candidates = [
    'https://geekyfarmers.com/wp-content/uploads/2021/10/header-hero-geekyfarmers-scaled.jpg',
    'https://geekyfarmers.com/wp-content/uploads/2021/10/header-hero-geekyfarmers.jpg',
    'https://geekyfarmers.com/wp-content/themes/geekyfarmers/images/hero.jpg',
  ];
  var hero = document.querySelector('.hero');
  var idx = 0;
  function tryNext() {
    if (idx >= candidates.length) return; // alla misslyckades, behåll grön
    var img = new Image();
    img.onload = function() {
      hero.style.backgroundImage =
        'linear-gradient(rgba(20,35,20,.52),rgba(20,35,20,.52)), url(' + candidates[idx] + ')';
    };
    img.onerror = function() { idx++; tryNext(); };
    img.src = candidates[idx];
  }
  tryNext();
})();

"""

old = "\n// ═══════════════════════════════════════════\n// START"
new = hero_js + "\n// ═══════════════════════════════════════════\n// START"
if old in content:
    content = content.replace(old, new, 1)
    changes += 1
    print("✓ Hero-bakgrundsbild JS tillagd")
else:
    # fallback: inject before last </script>
    content = content.replace("</script>\n</body>", hero_js + "</script>\n</body>", 1)
    changes += 1
    print("✓ Hero-bakgrundsbild JS tillagd (fallback-position)")

# ── Skriv fil ──
if changes > 0:
    open(src, "w", encoding="utf-8").write(content)
    print(f"\n✅ {changes} ändringar sparade till {src}")
else:
    print("\n⚠ Inga ändringar gjorda – kontrollera att rätt index.html används")
