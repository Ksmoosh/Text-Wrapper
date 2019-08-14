from bs4 import BeautifulSoup


class WrapperArticleParser(BeautifulSoup):
    def insert_after(self, successor):
        pass

    def insert_before(self, successor):
        pass

    def __init__(self, html):
        self.html_string = html
        self.soup = BeautifulSoup(html, "html.parser")
        self.articleCategories = []
        self.articleText = []
        self.get_categories()
        self.get_content()

    def get_categories(self):
        # search for the main <div> tag specifying the article
        for tag_div in self.soup.find_all('div', {'class': 'hero-wrap clearfix hero-16 tipi-row content-bg parallax'}):
            # search for <a> tag which includes the article classification
            for tag in tag_div.find_all('a', {'class': 'cat cat-with-bg'}):
                self.articleCategories.append(tag.getText())

    def get_content(self):
        # below are some phrases that appear in every article when web scraping with chosen tags, those are unwanted
        useless_text = ['Patronujemy', 'Zdjęcie główne artykułu pochodzi z', 'See also']

        # search for tags that have article's main content
        for tag in self.soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul'],  {'class': None}):
            # if none of the useless text has appeared in the scrapped then append the article content
            if sum([tag.getText().find(phrase) for phrase in useless_text]) == -len(useless_text):
                self.articleText.append([tag.getText(), tag.name])


