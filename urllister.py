from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WrapperURLHelper(BeautifulSoup):
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.urlsInA = []
        self.find_articles_urls()

    def is_url(self, url):                              # check if valid url
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def find_articles_urls(self):
        self.urlsInA = [a['href'] for a in self.soup.find_all('a', href=True) if self.is_url(a['href'])]

