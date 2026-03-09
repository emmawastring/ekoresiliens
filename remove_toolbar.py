import re
c = open('index.html', encoding='utf-8').read()
c = re.sub(r'\s*<div class="toolbar">\s*<div style="display:flex;align-items:center;gap:\.5rem;flex-wrap:wrap;">\s*</div>\s*</div>', '', c)
open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')