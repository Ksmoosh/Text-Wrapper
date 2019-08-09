import urllib.request
import urllister

sock = urllib.request.urlopen(urllib.request.Request('https://geek.justjoin.it', headers={'User-Agent': 'Mozilla/5.0'}))
parser = urllister.WrapperURLHelper(sock)
sock.close()

parser.urlsInA = list(dict.fromkeys(parser.urlsInA))            # remove duplicates
for i, url in enumerate(parser.urlsInA):
    print(str(i) + " " + url)


