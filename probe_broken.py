import requests
h = {'User-Agent': 'Mozilla/5.0'}

tests = [
    ('SLU kalender', 'https://www.slu.se/om-slu/kalender/'),
    ('SLU evenemang', 'https://www.slu.se/evenemang/'),
    ('SLU sok', 'https://www.slu.se/sok/?q=evenemang'),
    ('SKS kalender', 'https://www.skogsstyrelsen.se/kalender/'),
    ('SKS evenemang', 'https://www.skogsstyrelsen.se/evenemang/'),
    ('SKS kurs', 'https://www.skogsstyrelsen.se/kurs-och-utbildning/'),
    ('HaV kalender', 'https://www.havochvatten.se/om-myndigheten/kalender.html'),
    ('HaV evenemang', 'https://www.havochvatten.se/evenemang/'),
    ('HaV nyheter', 'https://www.havochvatten.se/om-myndigheten/press-och-nyheter/'),
    ('Lst Skane', 'https://www.lansstyrelsen.se/skane/om-oss/kalender/kalenderhandelser---skane/'),
    ('Lst Skane ny', 'https://www.lansstyrelsen.se/skane/om-oss/kalender/'),
    ('Agroforestry', 'https://agroforestrysverige.se/evenemang/'),
]

for name, url in tests:
    try:
        r = requests.get(url, headers=h, timeout=8)
        print(f'{r.status_code} {name}: {url}')
    except Exception as e:
        print(f'ERR {name}: {e}')