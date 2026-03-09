import re
c = open('index.html', encoding='utf-8').read()

# Ta bort de två stat-link blocken i HTML
c = re.sub(r'\s*<a class="stat-link".*?</a>', '', c, flags=re.DOTALL)

# Ta bort stat-link CSS
c = re.sub(r'\.stat-link\{.*?\}', '', c)
c = re.sub(r'\.stat-link:hover\{.*?\}', '', c)
c = re.sub(r'\.stat-link \.stat-num\{.*?\}', '', c)
c = re.sub(r'\.stat-link \.stat-label\{.*?\}', '', c)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')