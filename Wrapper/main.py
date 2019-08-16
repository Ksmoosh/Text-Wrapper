import urllib.request
import URLlister
import ContentRetriever
import json
import BagOfWordsCreater


def create_socket(url):
    return urllib.request.urlopen(urllib.request.Request(url,
                                                         headers={'User-Agent': 'Mozilla/5.0'}))


def write_string_to_json(articleTXT, filename):
    with open(filename, 'w') as outfile:
        json.dump(articleTXT, outfile)


def open_json_to_string(articleTXT):
    with open(articleTXT) as infile:
        return json.load(infile)


if __name__ == '__main__':
    tryb = 2
    if tryb == 1:
        sock = create_socket('https://geek.justjoin.it')
        MainPage = URLlister.WrapperURLHelper(sock)
        sock.close()

        for i, url in enumerate(MainPage.articlesUrls):
            if i == 2:
                sock = create_socket(url)

                print(url)
                article = ContentRetriever.WrapperArticleParser(sock.read())

                sock.close

                write_string_to_json(article.articleText, 'article.txt')

                for cat in article.articleCategories:
                    print(cat)
                for text in article.articleText:
                    print(text[0])
                break
    else:
        artText = open_json_to_string("article.txt")
        bag = BagOfWordsCreater.BagOfWords([text[0] for text in artText])
        print([text[0] for text in artText])
        print(bag.articleExtracted)
