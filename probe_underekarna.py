import requests
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

for url in [
    'https://www.underekarna.se/p%C3%A5-g%C3%A5ng/',
    'https://www.underekarna.se/f%C3%B6r%C3%A4dling/',
    'https://www.underekarna.se/historia/',
    'https://www.youtube.com/@plockhugget/videos',
]:
    r = requests.get(url, headers=h, timeout=15)
    soup = BeautifulSoup(r.text, 'html.parser')
    print(f'=== {url} ({r.status_code}) ===')
    print(soup.get_text()[:500])
    print()