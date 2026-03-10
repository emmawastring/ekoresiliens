import requests
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from .base import BaseScraper

SOURCE_ID   = "alternativnu"
SOURCE_NAME = "Alternativ.nu"
BASE_URL    = "https://www.alternativ.nu"
FORUM_URL   = "https://www.alternativ.nu/index.php"
HEADERS     = {"User-Agent": "Mozilla/5.0"}

class AlternativnuScraper(BaseScraper):
    source_id   = SOURCE_ID
    name        = SOURCE_NAME

    def fetch(self):
        events = []
        # Hämta händelser för de kommande 6 månaderna
        now = datetime.now()
        months_to_scrape = []
        for i in range(6):
            d = now + timedelta(days=30*i)
            months_to_scrape.append((d.year, d.month))

        seen_urls = set()

        for year, month in months_to_scrape:
            # Hämta månadskalender för att hitta dagar med events
            cal_url = f"{BASE_URL}/index.php?action=calendar;viewlist;year={year};month={month:02d}"
            try:
                r = requests.get(cal_url, headers=HEADERS, timeout=15)
                r.raise_for_status()
                soup = BeautifulSoup(r.text, 'html.parser')

                # Hitta dagar med events
                event_days = soup.find_all('td', class_='events')
                for td in event_days:
                    a = td.find('a', href=True)
                    if not a:
                        continue
                    day_url = a['href']
                    if not day_url.startswith('http'):
                        day_url = BASE_URL + day_url

                    # Hämta dagssidan
                    try:
                        r2 = requests.get(day_url, headers=HEADERS, timeout=15)
                        r2.raise_for_status()
                        soup2 = BeautifulSoup(r2.text, 'html.parser')

                        for li in soup2.find_all('li', class_='windowbg'):
                            title_el = li.find('strong', class_='event_title')
                            if not title_el:
                                continue

                            link_el = title_el.find('a', href=True)
                            if not link_el:
                                continue

                            url = link_el['href']
                            if not url.startswith('http'):
                                url = BASE_URL + url
                            if url in seen_urls:
                                continue
                            seen_urls.add(url)

                            # Region/prefix i span
                            region = ""
                            span = title_el.find('span')
                            if span:
                                region = span.get_text(strip=True)

                            title = link_el.get_text(strip=True)
                            if region:
                                title = f"{region} – {title}"

                            # Datum från time[datetime]
                            time_el = li.find('time', datetime=True)
                            date_iso = None
                            if time_el:
                                dt_str = time_el['datetime']
                                m = re.match(r'(\d{4}-\d{2}-\d{2})', dt_str)
                                if m:
                                    date_iso = m.group(1)

                            if not date_iso:
                                continue

                            # Plats – text efter sista <br>
                            desc = li.get_text(' ', strip=True)

                            events.append(self.event(
                                title=title,
                                date_iso=date_iso,
                                url=url,
                                description=desc,
                                categories=["omstallning"],
                            ))
                    except Exception as e:
                        print(f"  {SOURCE_NAME}: fel dag {day_url}: {e}")
            except Exception as e:
                print(f"  {SOURCE_NAME}: fel månad {year}-{month}: {e}")

        return events