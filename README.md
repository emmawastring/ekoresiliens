# 🌿 Ekoresiliens

Automatisk aggregator för gratis webbinarier och kunskapsresurser om hållbarhet, klimat, biologisk mångfald, agroforestry och skogsträdgårdar – från SLU, Naturvårdsverket, Skogsstyrelsen, HaV, SMHI och fler.

**[→ Se sajten live](https://emmawastring.github.io/ekoresiliens)**

---

## Hur det fungerar

```
GitHub Actions (dagligen kl 08:00)
        ↓
scrapers/run_all.py
        ↓  hämtar RSS + HTML från källorna
data/webinars.json  ←── uppdateras och committas automatiskt
        ↓
index.html läser JSON-filen med fetch() och renderar kort
```

- **Ingen server behövs** – sajten är statisk HTML + JavaScript
- **Data uppdateras automatiskt** varje dag via GitHub Actions
- **Kunskapsresurserna** (`data/knowledge_resources.json`) redigeras manuellt

---

## Komma igång lokalt

### 1. Klona repot
```bash
git clone https://github.com/emmawastring/ekoresiliens.git
cd ekoresiliens
```

### 2. Installera Python-beroenden
```bash
pip install -r requirements.txt
```

### 3. Kör scrapers manuellt
```bash
python -m scrapers.run_all
```
Detta skapar/uppdaterar `data/webinars.json`.

### 4. Öppna sajten lokalt
Eftersom `index.html` använder `fetch()` behöver du en lokal server (annars blockerar CORS):
```bash
# Med Python (enklast):
python -m http.server 8000
# Öppna sedan: http://localhost:8000
```

Eller använd **VSCode Live Server**-tillägget (högerklicka på `index.html` → "Open with Live Server").

---

## Projektstruktur

```
ekoresiliens/
│
├── index.html                  ← Hela frontend:en (en fil)
│
├── data/
│   ├── webinars.json           ← Auto-genereras av scrapers (committas av Actions)
│   └── knowledge_resources.json← Manuellt kurerade kunskapsresurser
│
├── scrapers/
│   ├── __init__.py
│   ├── run_all.py              ← Kör alla scrapers, sparar JSON
│   ├── base.py                 ← Basklass med hjälpmetoder
│   ├── slu.py
│   ├── naturvardsverket.py
│   ├── skogsstyrelsen.py
│   ├── hav.py
│   ├── smhi.py
│   ├── sverigesradio.py        ← Vetenskap & Allmänhet
│   ├── agroforestry.py
│   └── permakultur.py
│
├── .github/
│   └── workflows/
│       └── update-data.yml     ← GitHub Actions: kör dagligen
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Lägga till en ny källa

1. Skapa `scrapers/minkalla.py` som ärver `BaseScraper`:

```python
from .base import BaseScraper

class MinKallaScraper(BaseScraper):
    name = "Min Källa"
    source_id = "MK"
    base_url = "https://minkalla.se"
    RSS_URL = "https://minkalla.se/feed/"

    def fetch(self) -> list[dict]:
        events = []
        feed = feedparser.parse(self.RSS_URL)
        for entry in feed.entries:
            title = entry.get("title", "")
            if not self.is_relevant(title):
                continue
            # ... parsa datum, länk etc.
            events.append(self.event(
                title=title,
                date_iso="2025-06-15",
                url=entry.get("link", self.base_url),
                categories=["klimat"],
            ))
        return events
```

2. Importera och lägg till i `scrapers/run_all.py`:
```python
from scrapers.minkalla import MinKallaScraper
SCRAPERS = [..., MinKallaScraper()]
```

3. Lägg till i `SOURCE_LABELS` i `index.html`.

---

## Lägga till kunskapsresurser

Redigera `data/knowledge_resources.json` direkt. Varje post följer detta format:

```json
{
  "id": "kb99",
  "source": "MK",
  "source_name": "Min Källa",
  "type": "databas",
  "icon": "📊",
  "title": "Resursens namn",
  "desc": "Kort beskrivning av resursen.",
  "cats": ["klimat", "biodiv"],
  "url": "https://minkalla.se/databas"
}
```

Typvärden: `databas` · `verktyg` · `karta` · `rapport` · `guide` · `portal` · `natverk`

---

## Publicera på GitHub Pages

1. Gå till **Settings → Pages** i ditt repo
2. Välj **Source: Deploy from a branch**
3. Välj **Branch: main** och **Folder: / (root)**
4. Spara – sajten publiceras på `https://emmawastring.github.io/ekoresiliens`

GitHub Actions committar uppdaterad `data/webinars.json` varje dag, och GitHub Pages publicerar automatiskt de nya filerna.

---

## Manuell körning av GitHub Actions

Gå till **Actions → Uppdatera webbinarier → Run workflow** för att trigga en omedelbar uppdatering.

---

## Teknikstack

| Del | Teknik |
|-----|--------|
| Frontend | Vanilla HTML + CSS + JavaScript (ingen framework) |
| Dataformat | JSON |
| Scraping | Python, `requests`, `beautifulsoup4`, `feedparser` |
| Automatisering | GitHub Actions (cron) |
| Hosting | GitHub Pages (gratis) |

---

*Skapad av [Emma Wastring](https://github.com/emmawastring)*
