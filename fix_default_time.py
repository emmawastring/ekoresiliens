c = open('index.html', encoding='utf-8').read()

# Ändra default activeTime till 'future'
c = c.replace(
    "let activeCat = 'all', activeTime = 'all',",
    "let activeCat = 'all', activeTime = 'future',"
)

# Markera 'Kommande'-chip som active istället för 'Alla'
c = c.replace(
    '<div class="chip active" data-time="all"',
    '<div class="chip" data-time="all"'
)
c = c.replace(
    '<div class="chip" data-time="future"',
    '<div class="chip active" data-time="future"'
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')