import re

c = open('index.html', encoding='utf-8').read()

# Ta bort ALLT mellan <div class="hero"> och <h1> och ersätt med rent header
new_header = '''<div class="hero">
  <div style="display:flex;align-items:center;justify-content:center;margin-bottom:1.5rem;flex-wrap:wrap;gap:1rem;position:relative;z-index:2;">
    <div class="logo">Eko<span>resiliens</span></div>
    <a class="creator" href="https://geekyfarmers.com/" target="_blank" rel="noopener" style="display:flex;align-items:center;gap:.5rem;text-decoration:none;">
      <span style="font-size:.75rem;color:var(--sage);opacity:.8;">skapad av</span>
      <img class="creator-logo" src="https://geekyfarmers.com/bilder/header-logo.jpg" alt="Geeky Farmers" style="width:48px;height:48px;border-radius:50%;object-fit:cover;" onerror="this.style.display='none'">
      <span style="font-weight:600;color:var(--clay);font-size:1.3rem;font-family:'Playfair Display',serif;">Geeky Farmers</span>
    </a>
  </div>
  <h1>'''

c = re.sub(r'<div class="hero">.*?<h1>', new_header, c, count=1, flags=re.DOTALL)

open('index.html', 'w', encoding='utf-8').write(c)

# Verifiera
check = open('index.html').read()
creators = check.count('class="creator"')
print(f'Klar! Antal creator-element: {creators} (ska vara 1)')