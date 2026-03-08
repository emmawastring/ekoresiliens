content = open('index.html', encoding='utf-8').read()
start = content.find('<aside>')
end = content.find('</aside>') + len('</aside>')
aside = content[start:end]
open('aside_dump.txt', 'w', encoding='utf-8').write(aside)
print(f"Aside: {len(aside)} tecken, sparat till aside_dump.txt")