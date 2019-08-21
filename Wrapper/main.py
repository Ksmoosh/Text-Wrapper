import urllib.request
import URLlister
import ContentRetriever
import json
import GloveMaker
import os
import re
import KerasCategorization


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


def save_articles(articles, folder):
    folderName = folder
    for article in articles:
        for category in article[0]:
            # exchange the '/' character in the name of a category, so it will not be mistaken for folder separator
            category = re.sub(r'%s' % r'\/', "-", category)
            write_string_to_txt("\n".join([text[0] for text in article[1]]),
                                folderName + os.sep + category + os.sep + article[2])


def create_corpus():
    while 1:
        corpus = input("Create corpus for training your own vector? [y/n] ")
        if corpus == 'y':
            return True
        elif corpus != 'n':
            continue
        else:
            return False


def download_articles():
    while 1:
        download = input("Download new articles from the website? "
                         "If no, only articles downloaded before will be used in classification [y/n] ")
        if download == 'y':
            return True
        elif download != 'n':
            continue
        else:
            return False


def leave_program():
    while 1:
        leave = input("Do you want to continue with program [c] or leave [l] and create Glove vector? "
                      "(not necessary because there is already one provided) [c/l]")
        if leave == 'l':
            return True
        elif leave != 'c':
            continue
        else:
            return False


if __name__ == '__main__':
    download = download_articles()  # if True;
    # program will download articles from the website and save them in local folders

    create_glove = create_corpus()  # if True; program will provide data sufficient for creating a glove vector,
    # but a vector itself has to be created according to instructions written in readme.md

    articles = []  # list of articles in a form of [<category>, <text>, <title>]
    articlesSeparatedWords = []  # list of articles in a form of [<category>, <text from article with separated
    #                                                              words prepared for creating vector corpus>]
    if download:
        sock = create_socket('https://geek.justjoin.it')
        MainPage = URLlister.WrapperURLHelper(sock)
        sock.close()

        # iterate over all of the links to articles provided by URLlister
        for i, url in enumerate(MainPage.articlesUrls):
            sock = create_socket(url)

            print(url)

            # parse a raw html code to usable data from articles
            article = ContentRetriever.WrapperArticleParser(sock.read())

            sock.close

            if create_glove == 1:
                bag = GloveMaker.BagOfWords([text[0] for text in article.articleText])
                articlesSeparatedWords.append([article.articleCategories, bag.articleExtracted])

            print(article.articleTitle)

            articles.append([article.articleCategories, article.articleText, article.articleTitle])

        if create_glove:
            write_string_to_json(articlesSeparatedWords, 'articlesSepWords.json')

        write_string_to_json(articles, 'articles.json')
        save_articles(articles, "Artykuły")

    else:
        if create_glove:
            articlesSeparatedWords = open_json_to_string("articlesSepWords.json")
        articles = open_json_to_string("articles.json")

    if create_glove:
        GloveMaker.Glove(articlesSeparatedWords)
        # ask about leaving program if previously checked to create glove vector,
        # as one may want to use their own vector in categorization
        if leave_program():
            exit(0)

    # separated paragraphs to one string
    art = []
    for article in articles:
        art.append("\n".join([text[0] for text in article[1]]))

    predicted_categories = KerasCategorization.KerasModel(art).predicted_categories

    # predicted categories assigned to articles, then saved in a folder
    for i in range(len(articles)):
        articles[i][0] = [predicted_categories[i]]

    save_articles(articles, "Artykuły Klasyfikacja")





