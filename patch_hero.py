import re

content = open('index.html', encoding='utf-8').read()
original_len = len(content)

# 1. Ta bort hela tab-bar div
content = re.sub(r'\n<div class="tab-bar">.*?</div>', '', content, flags=re.DOTALL, count=1)
print("1. Tab-bar borttagen")

# 2. Ta bort <header>...</header>
content = re.sub(r'<header>.*?</header>\n?', '', content, flags=re.DOTALL, count=1)
print("2. Header-tagg borttagen")

# 3. Lagg till nav-rad overst i hero, fore h1
old_h1 = '  <h1>Gratis evenemang om<br><em>h\u00e5llbarhet &amp; natur</em></h1>'
new_h1 = (
    '  <div style="display:flex;align-items:center;justify-content:space-between;'
    'margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;position:relative;z-index:2;">\n'
    '    <div class="logo">Eko<span>resiliens</span></div>\n'
    '    <div style="display:flex;align-items:center;gap:1rem;">\n'
    '      <span class="updated-info" id="updatedInfo"></span>\n'
    '      <a class="btn-primary" href="https://github.com/emmawastring/ekoresiliens" '
    'target="_blank" rel="noopener">GitHub \u2197</a>\n'
    '    </div>\n'
    '  </div>\n'
    '  <h1>Gratis evenemang om<br><em>h\u00e5llbarhet &amp; natur</em></h1>'
)

if old_h1 in content:
    content = content.replace(old_h1, new_h1, 1)
    print("3. Nav inlagd i hero")
else:
    print("3. VARNING: h1 hittades ej - kontrollera manuellt")

# 4. Justera sticky-positioner nu nar header (68px) ar borta
content = content.replace('top:68px;z-index:99', 'top:0;z-index:99')
content = content.replace('top:116px;z-index:90', 'top:48px;z-index:90')
content = content.replace('top:134px', 'top:66px')
print("4. Sticky-positioner justerade")

open('index.html', 'w', encoding='utf-8').write(content)
print(f"\nKlar! {original_len} -> {len(content)} tecken")