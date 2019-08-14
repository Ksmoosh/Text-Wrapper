import urllib.request
import URLlister
import ContentRetriever


def create_socket(url):
    return urllib.request.urlopen(urllib.request.Request(url,
                                                         headers={'User-Agent': 'Mozilla/5.0'}))


if __name__ == '__main__':

    sock = create_socket('https://geek.justjoin.it')
    MainPage = URLlister.WrapperURLHelper(sock)
    sock.close()

    for i, url in enumerate(MainPage.articlesUrls):
        if i == 2:
            sock = create_socket(url)

            print(url)
            article = ContentRetriever.WrapperArticleParser(sock.read())

            sock.close

            for cat in article.articleCategories:
                print(cat)
            for text in article.articleText:
                print(text[0])
            break

