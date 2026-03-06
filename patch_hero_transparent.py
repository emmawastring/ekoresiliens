import re

content = open('index.html', encoding='utf-8').read()

# 1. Hero - ta bort egen bakgrund, bara behåll mörk overlay
# Hitta och ersätt hela hero-CSS-blocket
content = re.sub(
    r'(\.hero\{)[^}]*(background-size:cover;background-position:center;[^}]*)}',
    r'\1padding:3rem 2rem 2.5rem;text-align:center;position:relative;overflow:hidden;}',
    content, count=1
)
print("1. Hero-bakgrund borttagen")

# 2. Se till att hero::before är en mörk overlay (inte svg-mönstret som primär overlay)
# Lägg till en enkel mörk overlay på hero direkt
old_hero_style = 'padding:3rem 2rem 2.5rem;text-align:center;position:relative;overflow:hidden;}'
new_hero_style = 'padding:3rem 2rem 2.5rem;text-align:center;position:relative;overflow:hidden;background:rgba(15,25,15,.50);}'
content = content.replace(old_hero_style, new_hero_style, 1)
print("2. Mörk overlay på hero tillagd")

# 3. Ta bort GitHub-knappen (alla förekomster)
content = re.sub(
    r'\s*<a class="btn-primary" href="https://github\.com/emmawastring/ekoresiliens"[^>]+>GitHub[^<]+</a>',
    '', content
)
print("3. GitHub-knapp borttagen")

open('index.html', 'w', encoding='utf-8').write(content)
print("Klar!")