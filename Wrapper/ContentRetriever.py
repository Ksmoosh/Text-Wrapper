from bs4 import BeautifulSoup


class WrapperArticleParser(BeautifulSoup):
    def insert_after(self, successor):
        pass

    def insert_before(self, successor):
        pass

    def __init__(self, html):
        self.soup = BeautifulSoup(html, "html.parser")
        self.articleCategories = []
        self.get_categories()

    def get_categories(self):
        # search for the main <div> tag specifying the article
        for tag_div in self.soup.find_all('div', {'class': 'hero-wrap clearfix hero-16 tipi-row content-bg parallax'}):
            # search for <a> tag which includes the article classification
            for tag in tag_div.find_all('a', {'class': 'cat cat-with-bg'}):
                print(tag.getText())

