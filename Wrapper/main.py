import urllib.request
import URLlister
import ContentRetriever
import json
import GloveMaker
import os
import re


def create_socket(url):
    return urllib.request.urlopen(urllib.request.Request(url,
                                                         headers={'User-Agent': 'Mozilla/5.0'}))


def write_string_to_json(articleTXT, filename):
    with open(filename, 'w') as outfile:
        json.dump(articleTXT, outfile)


def open_json_to_string(articleTXT):
    with open(articleTXT) as infile:
        return json.load(infile)


def write_string_to_txt(text, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w") as f:
        f.write(text)


def save_articles(articles):
    for paragraph in articles[0][1]:
        print(paragraph[0])
    folderName = "Artykuły"
    for article in articles:
        for category in article[0]:
            category = re.sub(r'%s' % r'\/', "-", category)
            write_string_to_txt("\n".join([text[0] for text in article[1]]),
                                folderName + os.sep + category + os.sep + article[2])


if __name__ == '__main__':
    tryb = 2
    articles = []
    articlesSeparatedWords = []
    if tryb == 1:
        sock = create_socket('https://geek.justjoin.it')
        MainPage = URLlister.WrapperURLHelper(sock)
        sock.close()

        for i, url in enumerate(MainPage.articlesUrls):

            sock = create_socket(url)

            print(url)
            article = ContentRetriever.WrapperArticleParser(sock.read())

            sock.close

            # write_string_to_json(article.articleText, 'article.txt')

            bag = GloveMaker.BagOfWords([text[0] for text in article.articleText])

            print(article.articleTitle)

            articles.append([article.articleCategories, article.articleText, article.articleTitle])
            articlesSeparatedWords.append([article.articleCategories, bag.articleExtracted])

        # write_string_to_json(articlesSeparatedWords, 'articlesSepWords.json')
        write_string_to_json(articles, 'articles.json')

    else:
        # artText = open_json_to_string("articlesSepWords.json")
        # glove = GloveMaker.Glove(artText)
        articles = open_json_to_string("articles.json")
        save_articles(articles)


