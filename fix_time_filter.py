import re

c = open('index.html', encoding='utf-8').read()

# Ta bort hela panel-filter-bar blocket
c = re.sub(
    r'\s*<div class="panel-filter-bar">.*?</div>\s*</div>\s*\n',
    '\n',
    c, count=1, flags=re.DOTALL
)

# Ny tidpunkt-grupp
time_group = '''        <div class="filter-group">
          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Tidpunkt</div>
          <div class="filter-group-body">
            <div class="chip-group">
              <div class="chip active" data-time="all" onclick="selectTime(this)">Alla</div>
              <div class="chip" data-time="future" onclick="selectTime(this)">Kommande</div>
              <div class="chip" data-time="week" onclick="selectTime(this)">Denna vecka</div>
              <div class="chip" data-time="month" onclick="selectTime(this)">Denna månad</div>
            </div>
          </div>
        </div>
'''

# Sätt in före Kategorier-gruppen
c = c.replace(
    '        <div class="filter-group">\n          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Kategorier</div>',
    time_group + '        <div class="filter-group">\n          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Kategorier</div>',
    1
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')