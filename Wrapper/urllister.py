from bs4 import BeautifulSoup
from urllib.parse import urlparse


def is_url(url):                              # check if valid url
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


class WrapperURLHelper(BeautifulSoup):
    def insert_after(self, successor):
        pass

    def insert_before(self, successor):
        pass

    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.articlesUrls = []
        self.find_articles_urls()

    def find_articles_urls(self):
        for tag in self.soup.find_all('article'):       # find every <article> tag and then, find <a> tag with a href
            for anchor in tag.find_all('a', href=True):
                if is_url(anchor['href']):
                    self.articlesUrls.append(anchor['href'])
                break
        self.articlesUrls = list(dict.fromkeys(self.articlesUrls))  # remove duplicated links
        return
