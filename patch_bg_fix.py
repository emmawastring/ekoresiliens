import re

content = open('index.html', encoding='utf-8').read()

# 1. Fixa bakgrunden - no-repeat och stretch
old = (
    'background-image:url(https://geekyfarmers.com/bilder/bakgrund.jpg);'
    'background-size:cover;background-position:center top;background-attachment:fixed;}'
)
new = (
    'background-image:url(https://geekyfarmers.com/bilder/bakgrund.jpg);'
    'background-size:cover;background-position:center top;background-repeat:no-repeat;'
    'background-attachment:fixed;}'
)
if old in content:
    content = content.replace(old, new, 1)
    print("1. background-repeat:no-repeat tillagd")
else:
    print("1. VARNING: body bakgrund hittades ej")

# 2. Ta bort GitHub-knappen
old_gh = '      <a class="btn-primary" href="https://github.com/emmawastring/ekoresiliens" target="_blank" rel="noopener">GitHub \u2197</a>\n'
if old_gh in content:
    content = content.replace(old_gh, '', 1)
    print("2. GitHub-knapp borttagen")
else:
    # prova utan newline
    old_gh2 = '<a class="btn-primary" href="https://github.com/emmawastring/ekoresiliens" target="_blank" rel="noopener">GitHub \u2197</a>'
    result = re.sub(r'\s*<a class="btn-primary" href="https://github\.com/emmawastring/ekoresiliens"[^>]+>GitHub[^<]+</a>', '', content)
    if result != content:
        content = result
        print("2. GitHub-knapp borttagen (regex)")
    else:
        print("2. VARNING: GitHub-knapp hittades ej")

open('index.html', 'w', encoding='utf-8').write(content)
print("Klar!")
