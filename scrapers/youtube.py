import feedparser
from typing import List


class YouTubeScraper:
    """Simple helper to fetch latest videos from a YouTube channel RSS feed.

    Not a subclass of BaseScraper because it produces knowledge-resource objects
    rather than event dicts.
    """

    def __init__(self, channel_id: str, source_name: str | None = None):
        self.channel_id = channel_id
        self.source_name = source_name or channel_id
        # support full URLs, user handles or IDs
        if channel_id.startswith("http"):
            # strip to final part after /@
            if "@" in channel_id:
                handle = channel_id.split("@")[-1]
                self.feed_url = f"https://www.youtube.com/feeds/videos.xml?user={handle}"
            else:
                self.feed_url = channel_id
        elif channel_id.startswith("UC"):
            self.feed_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        else:
            # assume username
            self.feed_url = f"https://www.youtube.com/feeds/videos.xml?user={channel_id}"

    def fetch(self) -> List[dict]:
        entries: List[dict] = []
        d = feedparser.parse(self.feed_url)
        for e in d.entries:
            vid = e.get('yt_videoid') or e.get('id', '').split(':')[-1]
            title = e.get('title', '')
            url = e.get('link', '')
            desc = e.get('summary', '')
            published = e.get('published', '')
            date_iso = published[:10] if published else ''
            if vid and title and url:
                entries.append({
                    "id": f"yt_{vid}",
                    "source": self.source_name,
                    "source_name": self.source_name,
                    "type": "video",
                    "icon": "📺",
                    "title": title,
                    "desc": desc,
                    "cats": ["video"],
                    "url": url,
                })
        return entries
