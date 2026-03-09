c = open('index.html', encoding='utf-8').read()

# Fix Typ-gruppen - lägg till toggleFilterGroup och filter-group-body
c = c.replace(
    '          <div class="filter-group-label">Typ</div>\n          <div class="chip-group" id="kbTypeChips">',
    '          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Typ</div>\n          <div class="filter-group-body">\n          <div class="chip-group" id="kbTypeChips">'
)
c = c.replace(
    '            <div class="chip" data-kbtype="video"         onclick="selectKBType(this)">Video</div>\n          </div>\n        </div>\n\n        <div class="filter-group">\n          <div class="filter-group-label">Kategori</div>',
    '            <div class="chip" data-kbtype="video"         onclick="selectKBType(this)">Video</div>\n          </div>\n          </div>\n        </div>\n\n        <div class="filter-group">\n          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Kategori</div>'
)

# Fix Kategori-gruppen - lägg till filter-group-body
c = c.replace(
    '          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Kategori</div>\n          <div class="chip-group" id="kbCatChips">',
    '          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Kategori</div>\n          <div class="filter-group-body">\n          <div class="chip-group" id="kbCatChips">'
)

# Stäng filter-group-body efter kbCatChips (före Språk-gruppen)
c = c.replace(
    '            <div class="chip" data-cat="sparade"           onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#d47c52"></span>Sparade webbinarier</div>\n          </div>\n        </div>\n\n        <div class="filter-group">\n          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Språk</div>',
    '            <div class="chip" data-cat="sparade"           onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#d47c52"></span>Sparade webbinarier</div>\n          </div>\n          </div>\n        </div>\n\n        <div class="filter-group">\n          <div class="filter-group-label" onclick="toggleFilterGroup(this)">Språk</div>'
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')