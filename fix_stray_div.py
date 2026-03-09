c = open('index.html', encoding='utf-8').read()

# Ta bort den lösa </div> som stänger panel-webbinarier för tidigt
c = c.replace(
    '<div class="tab-panel active" id="panel-webbinarier">\n  </div>\n  <div class="main-wrap">',
    '<div class="tab-panel active" id="panel-webbinarier">\n  <div class="main-wrap">',
    1
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')