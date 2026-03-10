c = open('index.html', encoding='utf-8').read()

# === EVENEMANG-sidan: catChips ===
old_cats = '''            <div class="chip-group" id="catChips">
              <div class="chip active" data-cat="all" onclick="selectCat(this,'catChips')">Alla</div>
              <div class="chip" data-cat="klimat" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#1b6b4e"></span>Klimat</div>
              <div class="chip" data-cat="biodiv" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#2e7d32"></span>Biologisk mångfald</div>
              <div class="chip" data-cat="samhalle" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#e65100"></span>Samhälle</div>
              <div class="chip" data-cat="vatten" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#1565c0"></span>Vatten</div>
              <div class="chip" data-cat="skog" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#33691e"></span>Skog</div>
              <div class="chip" data-cat="mat" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#880e4f"></span>Mat &amp; Jordbruk</div>
              <div class="chip" data-cat="energi" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#f57f17"></span>Energi</div>
              <div class="chip" data-cat="policy" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#4527a0"></span>Policy</div>
              <div class="chip" data-cat="agroforestry" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#2d6a2d"></span>Agroforestry</div>'''

new_cats = '''            <div class="chip-group" id="catChips">
              <div class="chip active" data-cat="all" onclick="selectCat(this,'catChips')">Alla</div>
              <div class="chip" data-cat="omstallning" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#e65100"></span>Omställning &amp; Resiliens</div>
              <div class="chip" data-cat="beredskap" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#b71c1c"></span>Beredskap</div>
              <div class="chip" data-cat="klimat" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#1b6b4e"></span>Klimat &amp; Klimatanpassning</div>
              <div class="chip" data-cat="mat" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#880e4f"></span>Mat &amp; Självhushållning</div>
              <div class="chip" data-cat="biodiv" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#2e7d32"></span>Biologisk mångfald</div>
              <div class="chip" data-cat="skog" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#33691e"></span>Skog</div>
              <div class="chip" data-cat="agroforestry" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#2d6a2d"></span>Agroforestry</div>
              <div class="chip" data-cat="skogstradgard" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#1a5c1a"></span>Skogsträdgård</div>
              <div class="chip" data-cat="vatten" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#1565c0"></span>Vatten</div>
              <div class="chip" data-cat="energi" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#f57f17"></span>Energi</div>
              <div class="chip" data-cat="policy" onclick="selectCat(this,'catChips')"><span class="chip-dot" style="background:#4527a0"></span>Lag &amp; Policy</div>'''

c = c.replace(old_cats, new_cats, 1)

# === KB-sidan: kbCatChips ===
old_kb = '''            <div class="chip active" data-cat="all"           onclick="selectCat(this,'kbCatChips')">Alla</div>
            <div class="chip" data-cat="klimat"               onclick="selectCat(this,'kbCatChips')"><span class="chip-dot" style="background:#1b6b4e"></span>Klimat</div>'''

new_kb = '''            <div class="chip active" data-cat="all"           onclick="selectCat(this,'kbCatChips')">Alla</div>
            <div class="chip" data-cat="omstallning"          onclick="selectCat(this,'kbCatChips')"><span class="chip-dot" style="background:#e65100"></span>Omställning &amp; Resiliens</div>
            <div class="chip" data-cat="beredskap"            onclick="selectCat(this,'kbCatChips')"><span class="chip-dot" style="background:#b71c1c"></span>Beredskap</div>
            <div class="chip" data-cat="klimat"               onclick="selectCat(this,'kbCatChips')"><span class="chip-dot" style="background:#1b6b4e"></span>Klimat &amp; Klimatanpassning</div>'''

c = c.replace(old_kb, new_kb, 1)

# Uppdatera "Samhälle" → "Omställning & Resiliens" i kbCatChips
c = c.replace(
    '<div class="chip" data-cat="samhalle"             onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#e65100"></span>Samhälle</div>',
    '<div class="chip" data-cat="samhalle"             onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#e65100"></span>Omställning &amp; Resiliens</div>'
)

# Uppdatera Policy → Lag & Policy i kbCatChips
c = c.replace(
    '<div class="chip" data-cat="policy"               onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#4527a0"></span>Policy</div>',
    '<div class="chip" data-cat="policy"               onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#4527a0"></span>Lag &amp; Policy</div>'
)

# Uppdatera Mat & Jordbruk → Mat & Självhushållning i kbCatChips
c = c.replace(
    '<div class="chip" data-cat="mat"                  onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#880e4f"></span>Mat &amp; Jordbruk</div>',
    '<div class="chip" data-cat="mat"                  onclick="selectCat(this,\'kbCatChips\')"><span class="chip-dot" style="background:#880e4f"></span>Mat &amp; Självhushållning</div>'
)

open('index.html', 'w', encoding='utf-8').write(c)
print('Klar!')