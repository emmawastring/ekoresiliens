import re

content = open('index.html', encoding='utf-8').read()
changes = 0

# ══════════════════════════════════════════
# 1. Lägg tillbaka "skapad av Geeky Farmers" i hero-nav-raden
# ══════════════════════════════════════════
old_nav = (
    '    <div class="logo">Eko<span>resiliens</span></div>\n'
    '    <div style="display:flex;align-items:center;gap:1rem;">\n'
    '      <span class="updated-info" id="updatedInfo"></span>\n'
    '      <a class="btn-primary" href="https://github.com/emmawastring/ekoresiliens"'
    ' target="_blank" rel="noopener">GitHub \u2197</a>\n'
    '    </div>'
)
new_nav = (
    '    <div class="logo">Eko<span>resiliens</span></div>\n'
    '    <div style="display:flex;align-items:center;gap:1.2rem;">\n'
    '      <a class="creator" href="https://geekyfarmers.com/" target="_blank" rel="noopener">\n'
    '        <span style="font-size:.75rem;color:var(--sage);opacity:.8;">skapad av</span>\n'
    '        <img class="creator-logo" src="https://geekyfarmers.com/bilder/header-logo.jpg"'
    ' alt="Geeky Farmers" onerror="this.style.display=\'none\'">\n'
    '        <span style="font-weight:600;color:var(--clay);font-size:1.5rem;'
    'font-family:\'Playfair Display\',serif;">Geeky Farmers</span>\n'
    '      </a>\n'
    '      <span class="updated-info" id="updatedInfo"></span>\n'
    '      <a class="btn-primary" href="https://github.com/emmawastring/ekoresiliens"'
    ' target="_blank" rel="noopener">GitHub \u2197</a>\n'
    '    </div>'
)
if old_nav in content:
    content = content.replace(old_nav, new_nav, 1)
    changes += 1
    print("1. Geeky Farmers-badge återlagd")
else:
    print("1. VARNING: nav-raden hittades ej")

# ══════════════════════════════════════════
# 2. Body – bakgrundsbild hela sidan
# ══════════════════════════════════════════
old_body = 'body{font-family:\'DM Sans\',sans-serif;background:var(--cream);color:var(--charcoal);min-height:100vh;}'
new_body = (
    'body{font-family:\'DM Sans\',sans-serif;background:var(--charcoal);color:var(--charcoal);min-height:100vh;'
    'background-image:url(https://geekyfarmers.com/bilder/bakgrund.jpg);'
    'background-size:cover;background-position:center top;background-attachment:fixed;}'
)
if old_body in content:
    content = content.replace(old_body, new_body, 1)
    changes += 1
    print("2. Bakgrundsbild på body tillagd")
else:
    print("2. VARNING: body CSS hittades ej")

# ══════════════════════════════════════════
# 3. Hero – ta bort egen bakgrundsfärg (body-bilden syns igenom)
# ══════════════════════════════════════════
content = re.sub(
    r'(\.hero\{)background:var\(--moss\);background-image:[^;]+;',
    r'\1',
    content, count=1
)
# Lägg till mörk overlay i hero::before istället
old_before = ".hero::before{content:'';position:absolute;inset:0;background-image:url(\"data:image/svg+xml"
new_before = ".hero::before{content:'';position:absolute;inset:0;background:rgba(15,25,15,.45);z-index:0;}\n.hero::after{content:'';position:absolute;inset:0;background-image:url(\"data:image/svg+xml"
if old_before in content:
    content = content.replace(old_before, new_before, 1)
    # Stäng ::after korrekt
    content = content.replace(".hero::before{content:'';position:absolute;inset:0;background-image:url(\"data:image/svg+xml", ".hero::after{content:'';position:absolute;inset:0;background-image:url(\"data:image/svg+xml", 1)
changes += 1
print("3. Hero-bakgrund transparent (body-bild syns)")

# ══════════════════════════════════════════
# 4. Paneler – semi-transparenta
# ══════════════════════════════════════════

# filter-card
old_fc = '.filter-card{background:#fff;border:1px solid var(--mist);border-radius:16px;padding:1.4rem;margin-bottom:1rem;box-shadow:0 2px 12px rgba(58,90,64,.06);}'
new_fc = '.filter-card{background:rgba(245,240,232,.88);border:1px solid rgba(163,184,153,.4);border-radius:16px;padding:1.4rem;margin-bottom:1rem;box-shadow:0 4px 20px rgba(0,0,0,.15);backdrop-filter:blur(6px);}'
if old_fc in content:
    content = content.replace(old_fc, new_fc, 1)
    changes += 1
    print("4a. filter-card transparent")

# event cards
old_card = 'a.card{background:#fff;border:1px solid var(--mist);border-radius:16px;overflow:hidden;box-shadow:0 2px 12px rgba(58,90,64,.05);transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column;text-decoration:none;color:inherit;cursor:pointer;}'
new_card = 'a.card{background:rgba(250,247,242,.90);border:1px solid rgba(163,184,153,.35);border-radius:16px;overflow:hidden;box-shadow:0 4px 18px rgba(0,0,0,.18);transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column;text-decoration:none;color:inherit;cursor:pointer;backdrop-filter:blur(4px);}'
if old_card in content:
    content = content.replace(old_card, new_card, 1)
    changes += 1
    print("4b. event cards transparenta")

# kb cards
old_kb = '.kb-card{background:#fff;border:1px solid var(--mist);border-radius:14px;padding:1.1rem;box-shadow:0 2px 10px rgba(58,90,64,.04);transition:transform .15s,box-shadow .15s;display:flex;flex-direction:column;gap:.5rem;text-decoration:none;color:inherit;cursor:pointer;}'
new_kb = '.kb-card{background:rgba(250,247,242,.90);border:1px solid rgba(163,184,153,.35);border-radius:14px;padding:1.1rem;box-shadow:0 4px 18px rgba(0,0,0,.18);transition:transform .15s,box-shadow .15s;display:flex;flex-direction:column;gap:.5rem;text-decoration:none;color:inherit;cursor:pointer;backdrop-filter:blur(4px);}'
if old_kb in content:
    content = content.replace(old_kb, new_kb, 1)
    changes += 1
    print("4c. kb-cards transparenta")

# filter-bar
old_fb = '.panel-filter-bar{background:#fff;border-bottom:1px solid var(--mist);padding:.7rem 2rem;display:flex;align-items:center;gap:.8rem;flex-wrap:wrap;position:sticky;top:116px;z-index:90;box-shadow:0 2px 8px rgba(58,90,64,.04);}'
new_fb = '.panel-filter-bar{background:rgba(245,240,232,.85);border-bottom:1px solid rgba(163,184,153,.3);padding:.7rem 2rem;display:flex;align-items:center;gap:.8rem;flex-wrap:wrap;position:sticky;top:0;z-index:90;box-shadow:0 2px 12px rgba(0,0,0,.12);backdrop-filter:blur(8px);}'
if old_fb in content:
    content = content.replace(old_fb, new_fb, 1)
    changes += 1
    print("4d. filter-bar transparent")

# cream bakgrund på main-wrap
old_mw = '.main-wrap{max-width:1280px;margin:0 auto;padding:2rem;display:flex;gap:2rem;align-items:flex-start;}'
new_mw = '.main-wrap{max-width:1280px;margin:0 auto;padding:2rem;display:flex;gap:2rem;align-items:flex-start;}'
# background är redan transparent via body

# search boxes
content = content.replace('background:var(--cream) url(', 'background:rgba(245,240,232,.9) url(')
content = content.replace('background:#fff url(', 'background:rgba(255,255,255,.9) url(')

open('index.html', 'w', encoding='utf-8').write(content)
print(f"\nKlar! {changes} ändringar sparade")