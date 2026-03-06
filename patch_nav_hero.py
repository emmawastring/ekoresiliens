content = open('index.html', encoding='utf-8').read()

old = '<h1>Samlade evenemang och kunskapsresurser om<br><em>h\u00e5llbarhet & natur</em></h1>'
new = (
    '<div style="display:flex;align-items:center;justify-content:space-between;'
    'margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;position:relative;z-index:2;">\n'
    '    <div class="logo">Eko<span>resiliens</span></div>\n'
    '    <div style="display:flex;align-items:center;gap:1rem;">\n'
    '      <span class="updated-info" id="updatedInfo"></span>\n'
    '      <a class="btn-primary" href="https://github.com/emmawastring/ekoresiliens"'
    ' target="_blank" rel="noopener">GitHub \u2197</a>\n'
    '    </div>\n'
    '  </div>\n'
    '  <h1>Samlade evenemang och kunskapsresurser om<br><em>h\u00e5llbarhet & natur</em></h1>'
)

if old in content:
    content = content.replace(old, new, 1)
    open('index.html', 'w', encoding='utf-8').write(content)
    print("Klar! Nav inlagd i hero.")
else:
    print("VARNING: h1 hittades ej")