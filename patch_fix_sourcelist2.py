content = open('index.html', encoding='utf-8').read()

old = (
    'buttonDiv.innerHTML = `\n'
    '    <button style="font-size:.75rem;padding:4px 8px;background:#588157;color:#fff;border:none;border-radius:6px;cursor:pointer;width:100%;font-weight:500" onclick="toggleAllSources()">V\u00e4lj alla</button>`;\n'
    '  list.appendChild(buttonDiv);\n'
    '  \n'
    '  // Inkludera alla k\u00e4nda'
)
new = '  // Inkludera alla k\u00e4nda'

# Ta bort lite mer context - hela buttonDiv-blocket
import re
pattern = r"  const buttonDiv = document\.createElement\('div'\);\n  buttonDiv\.style\.marginBottom = '0\.7rem';\n  buttonDiv\.innerHTML = `\n    <button[^`]+toggleAllSources\(\)[^`]+`;\n  list\.appendChild\(buttonDiv\);\n  \n"
result = re.sub(pattern, '  ', content, count=1)

if result != content:
    content = result
    open('index.html', 'w', encoding='utf-8').write(content)
    print("Klar! Knapp borttagen.")
else:
    print("VARNING: Hittades ej med regex heller")
    # Sista utväg - hitta och visa exakt vad som finns
    idx = content.find("toggleAllSources()")
    print(repr(content[idx-300:idx+50]))