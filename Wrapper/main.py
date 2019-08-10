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
        sock = create_socket(url)

        print(url)
        article = ContentRetriever.WrapperArticleParser(sock)

        sock.close

