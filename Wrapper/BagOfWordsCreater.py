import json
import re


def open_json_to_string(filename):
    with open(filename) as infile:
        return json.load(infile)


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
        # sort alphabetically
        self.articleExtracted = sorted(list(set(self.articleExtracted)))
