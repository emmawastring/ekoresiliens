import requests
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

for url in [
    'https://www.underekarna.se/p%C3%A5-g%C3%A5ng/',
    'https://www.underekarna.se/f%C3%B6r%C3%A4dling/',
    'https://www.underekarna.se/historia/',
]:
    r = requests.get(url, headers=h, timeout=15)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text, 'html.parser')
    print(f'=== {url} ===')
    # Kolla artikel/post-strukturen
    articles = soup.select('article, .post, .entry, .event, main')
    print(f'  article-element: {len(articles)}')
    if articles:
        print(articles[0].get_text()[:300])
    # Kolla h2/h3
    headers = soup.select('h2, h3')
    print(f'  rubriker: {len(headers)}')
    for hh in headers[:3]:
        a = hh.find('a')
        print(f'    {hh.get_text(strip=True)[:60]}', '|', a.get('href','')[:60] if a else '')
    print()