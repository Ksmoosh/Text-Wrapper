import urllib.request
import urllister

sock = urllib.request.urlopen(urllib.request.Request('https://geek.justjoin.it', headers={'User-Agent': 'Mozilla/5.0'}))
parser = urllister.WrapperURLHelper(sock)
sock.close()

parser.articlesUrls = list(dict.fromkeys(parser.articlesUrls))            # remove duplicates
for i, url in enumerate(parser.articlesUrls):
    print(str(i) + " " + url)


