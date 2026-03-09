import re
c = open('index.html', encoding='utf-8').read()

replacement = '''  <div style="display:grid;grid-template-columns:1fr auto 1fr;align-items:center;margin-bottom:1.5rem;position:relative;z-index:2;">
    <div></div>
    <div class="logo">Eko<span>resiliens</span></div>
    <a class="creator" href="https://geekyfarmers.com/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:.5rem;text-decoration:none;justify-content:flex-end;">
      <span style="font-size:.75rem;color:var(--sage);opacity:.8;">skapad av</span>
      <img class="creator-logo" src="https://geekyfarmers.com/bilder/header-logo.jpg" alt="Geeky Farmers" style="width:48px;height:48px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
      <span style="font-weight:600;color:var(--clay);font-size:1.3rem;font-family:'Playfair Display',serif;">Geeky Farmers</span>
    </a>
  </div>'''

c = re.sub(
    r'  <div style="display:flex;align-items:center;justify-content:center.*?</div>',
    replacement,
    c, count=1, flags=re.DOTALL
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!' if 'grid-template-columns' in open('index.html').read() else 'Ingen match!')