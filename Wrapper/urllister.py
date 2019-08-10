from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WrapperURLHelper(BeautifulSoup):
    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.articlesUrls = []
        self.find_articles_urls()

    def is_url(self, url):                              # check if valid url
        try:
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except ValueError:
            return False

    def find_articles_urls(self):
        for tag in self.soup.find_all('article'):       # find every <article> tag and then, find <a> tag with a href
            for anchor in tag.find_all('a', href=True):
                self.articlesUrls.append(anchor['href'])
                break
        return
