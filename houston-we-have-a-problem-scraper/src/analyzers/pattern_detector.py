import requests
from bs4 import BeautifulSoup

class PatternDetector:
    def __init__(self, settings):
        self.settings = settings
        self.timeout = settings.get("timeout", 10)

    def fetch_data(self, url):
        response = requests.get(url, timeout=self.timeout)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, "html.parser")
        return {
            "url": url,
            "title": soup.title.string if soup.title else None,
            "content": soup.get_text(strip=True)
        }