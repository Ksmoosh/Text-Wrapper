import json
import re
import os


def open_json_to_string(filename):
    with open(filename) as infile:
        return json.load(infile)


def write_string_to_txt(text, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(text)


def right_word(w):
    # starts with a letter
    if re.match("^[a-zA-Z]", w):
        return True
    return False


class BagOfWords:
    def __init__(self, article):
        self.stopWords = open_json_to_string("stopwords-pl.json")
        self.article = article
        self.articleExtracted = []
        self.words_extraction(self.article)

    def words_extraction(self, article):
        # split article to paragraphs and extract polish stop words from them
        articleParagraphed = []
        for paragraph in article:
            words = re.sub("[^\w]", " ", paragraph).split()
            articleParagraphed.append([w.lower() for w in words if w not in self.stopWords and right_word(w)])
        # join sentences separated in different lists to one list of strings for whole article
        self.articleExtracted = [j for sub in articleParagraphed for j in sub]


class Glove:
    def __init__(self, articlesSeparatedWords):
        self.articlesSep = articlesSeparatedWords
        self.if_create_corpus()

    def if_create_corpus(self):
        while 1:
            vector = input("Create corpus for training your own vector? [y/n]")
            if vector == 'y':
                self.create_corpus()
                break
            elif vector != 'n':
                continue
            else:
                break

    def check_categories(self):
        categories = []
        # check for unique categories in articles
        for article in self.articlesSep:
            for category in article[0]:
                categories.append(category)
        return sorted(list(set(categories)))

    def divide_by_categories(self, categories):
        corpus = []
        # for every category assign right articles
        for category in categories:
            text = []
            for article in self.articlesSep:
                if category in article[0]:
                    text.append(article[1])
            text = " ".join([j for sub in text for j in sub])
            corpus.append([category, text])
        return corpus

    def create_corpus(self):
        categories = self.check_categories()

        corpusList = self.divide_by_categories(categories)

        corpus = "\n".join([text[1] for text in corpusList])

        write_string_to_txt(corpus, "glove" + os.sep + "corpus.txt")

