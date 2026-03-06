import re

content = open('index.html', encoding='utf-8').read()

# Hitta body-regeln och lägg till fallback-färg + fixa background-color
old = re.search(r'body\{[^}]+background-image:url\(https://geekyfarmers\.com/bilder/bakgrund\.jpg\)[^}]+\}', content)
if old:
    print("Hittad:", repr(old.group()[:100]))
    new = (
        'body{font-family:\'DM Sans\',sans-serif;color:var(--charcoal);min-height:100vh;'
        'background-color:#1e2a1e;'  # fallback = charcoal green
        'background-image:url(https://geekyfarmers.com/bilder/bakgrund.jpg);'
        'background-size:cover;background-position:center top;background-repeat:no-repeat;}'
    )
    content = content.replace(old.group(), new, 1)
    open('index.html', 'w', encoding='utf-8').write(content)
    print("Klar! Fallback-färg #1e2a1e (mörk grön) tillagd")
else:
    # Visa vad som finns
    idx = content.find('body{')
    print("body CSS:", repr(content[idx:idx+300]))
    