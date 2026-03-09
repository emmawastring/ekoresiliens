import requests, json

h = {'User-Agent': 'Mozilla/5.0'}

# Kolla om det finns press/rapport-typer
for slug in ['press', 'posts']:
    r = requests.get(f'https://hushallningssallskapet.se/wp-json/wp/v2/{slug}?per_page=2&_fields=id,date,title,link,categories,tags,type', headers=h)
    print(f'=== {slug} {r.status_code} ===')
    if r.status_code == 200:
        data = r.json()
        for item in data[:2]:
            print(json.dumps(item, ensure_ascii=False, indent=2)[:600])
    print()