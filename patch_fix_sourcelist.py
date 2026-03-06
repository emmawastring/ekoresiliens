content = open('index.html', encoding='utf-8').read()

# Ta bort den inbyggda "Välj alla"-knappen från buildSourceList
old = (
    "  // \"V\u00e4lj alla/Avmarkera alla\" knapp\n"
    "  const buttonDiv = document.createElement('div');\n"
    "  buttonDiv.style.marginBottom = '0.7rem';\n"
    "  buttonDiv.innerHTML = `\n"
    "    <button style=\"font-size:.75rem;padding:4px 8px;background:#588157;color:#fff;border:none;border-radius:6px;cursor:pointer;width:100%;font-weight:500\" onclick=\"toggleAllSources()\">V\u00e4lj alla</button>`;\n"
    "  list.appendChild(buttonDiv);\n"
    "  \n"
    "  // Inkludera alla k\u00e4nda k\u00e4llor"
)
new = "  // Inkludera alla k\u00e4nda k\u00e4llor"

if old in content:
    content = content.replace(old, new, 1)
    print("Knapp borttagen ur buildSourceList")
else:
    print("VARNING: hittades ej - kontrollera manuellt")

# Ta även bort samma knapp från buildKBSourceList
old_kb = (
    "  // \"V\u00e4lj alla/Avmarkera alla\" knapp\n"
    "  const buttonDiv = document.createElement('div');\n"
    "  buttonDiv.style.marginBottom = '0.7rem';\n"
    "  buttonDiv.innerHTML = `\n"
    "    <button style=\"font-size:.75rem;padding:4px 8px;background:#588157;color:#fff;border:none;border-radius:6px;cursor:pointer;width:100%;font-weight:500\" onclick=\"toggleAllKBSources()\">Avmarkera alla</button>`;\n"
    "  list.appendChild(buttonDiv);\n\n"
    "  // Inkludera alla k\u00e4llor fr\u00e5n kunskapsresurser"
)
new_kb = "  // Inkludera alla k\u00e4llor fr\u00e5n kunskapsresurser"

if old_kb in content:
    content = content.replace(old_kb, new_kb, 1)
    print("Knapp borttagen ur buildKBSourceList")
else:
    print("VARNING: KB-knapp hittades ej")

open('index.html', 'w', encoding='utf-8').write(content)
print("Klar!")