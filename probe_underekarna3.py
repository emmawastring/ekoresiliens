import requests
from bs4 import BeautifulSoup
h = {'User-Agent': 'Mozilla/5.0'}

# På gång - kolla allt innehåll
r = requests.get('https://www.underekarna.se/p%C3%A5-g%C3%A5ng/', headers=h)
r.encoding = 'utf-8'
soup = BeautifulSoup(r.text, 'html.parser')
print('=== PÅ GÅNG - hela main ===')
main = soup.find('main') or soup.find('body')
print(main.get_text()[:800])
print()

# Kolla om det finns iframe eller embed
iframes = soup.find_all('iframe')
print('Iframes:', len(iframes))
for i in iframes[:2]: print(i.get('src','')[:80])

print()

# Historia - kolla main
r2 = requests.get('https://www.underekarna.se/historia/', headers=h)
r2.encoding = 'utf-8'
soup2 = BeautifulSoup(r2.text, 'html.parser')
print('=== HISTORIA - main ===')
main2 = soup2.find('main') or soup2.find('body')
print(main2.get_text()[:1000])

# Förädling - kolla ett artikel-element
r3 = requests.get('https://www.underekarna.se/f%C3%B6r%C3%A4dling/', headers=h)
r3.encoding = 'utf-8'
soup3 = BeautifulSoup(r3.text, 'html.parser')
articles = soup3.select('article')
print()
print('=== FÖRÄDLING - artikel-element ===')
if articles:
    print(articles[0].prettify()[:500])