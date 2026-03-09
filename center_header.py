c = open('index.html', encoding='utf-8').read()

old = '''  <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;position:relative;z-index:2;">
    <div style="display:flex;align-items:center;gap:1rem;">
      <div class="logo">Eko<span>resiliens</span></div>
      <a class="creator" href="https://geekyfarmers.com/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:.5rem;text-decoration:none;">
        <span style="font-size:.75rem;color:var(--sage);opacity:.8;">skapad av</span>        <img class="creator-logo" src="https://geekyfarmers.com/bilder/header-logo.jpg" alt="Geeky Farmers" style="width:64px;height:64px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
        <span style="font-weight:600;color:var(--clay);font-size:1.5rem;font-family:'Playfair Display',serif;">Geeky Farmers</span>
      </a>
    </div>
  </div>'''

new = '''  <div style="display:flex;align-items:center;justify-content:center;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;position:relative;z-index:2;">
    <div class="logo">Eko<span>resiliens</span></div>
    <a class="creator" href="https://geekyfarmers.com/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:.5rem;text-decoration:none;">
      <span style="font-size:.75rem;color:var(--sage);opacity:.8;">skapad av</span>
      <img class="creator-logo" src="https://geekyfarmers.com/bilder/header-logo.jpg" alt="Geeky Farmers" style="width:48px;height:48px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
      <span style="font-weight:600;color:var(--clay);font-size:1.3rem;font-family:'Playfair Display',serif;">Geeky Farmers</span>
    </a>
  </div>'''

c = c.replace(old, new)
open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')