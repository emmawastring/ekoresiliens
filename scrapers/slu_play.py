"""SLU Play - Sparade webbinarier"""
from .base import BaseScraper


class SLUPlayScraper(BaseScraper):
    name = "SLU Play"
    source_id = "SLU Play"
    base_url = "https://play.slu.se"

    def fetch(self) -> list[dict]:
        events = []
        playlists = [
            "https://play.slu.se/playlist/details/0_04mppjet",
            "https://play.slu.se/playlist/details/0_keh1j1b6"
        ]

        for playlist_url in playlists:
            try:
                soup = self.soup(playlist_url)

                # Försök hitta spellistans titel
                playlist_title_elem = soup.select_one("h1, .playlist-title")
                playlist_title = playlist_title_elem.get_text(strip=True) if playlist_title_elem else "SLU Webbinarier"

                # Hitta alla videor i spellistan
                video_elements = soup.select(".video-item, .playlist-item, article")

                for element in video_elements:
                    title_elem = element.select_one("h3, h4, a, .video-title")
                    if not title_elem:
                        continue

                    title = title_elem.get_text(strip=True)
                    if not self.is_relevant(title):
                        continue

                    # För sparade webbinarier, använd dagens datum som "tillgänglig från"
                    # eftersom de är inspelade och tillgängliga
                    from datetime import datetime
                    date_str = datetime.now().strftime("%Y-%m-%d")

                    desc_elem = element.select_one("p, .description, .excerpt")
                    description = desc_elem.get_text(strip=True) if desc_elem else f"Från spellistan: {playlist_title}"

                    link_elem = element.select_one("a")
                    url = link_elem.get("href") if link_elem else playlist_url
                    if url and not url.startswith("http"):
                        url = self.base_url + url

                    events.append(self.event(
                        title=title,
                        date_iso=date_str,
                        url=url,
                        description=description,
                        categories=["samhalle", "biodiv", "mat", "skog"],
                    ))
            except Exception as e:
                print(f"    SLU Play ({playlist_url}): {e}")

        return events