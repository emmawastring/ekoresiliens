c = open('index.html', encoding='utf-8').read()
c = c.replace(
    "return d.toLocaleDateString('sv-SE', { weekday:'short', day:'numeric', month:'short' });",
    "return d.toLocaleDateString('sv-SE', { weekday:'short', day:'numeric', month:'short', year:'numeric' });"
)
open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')