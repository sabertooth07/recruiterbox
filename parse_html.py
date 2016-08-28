import urllib2
import Queue
import argparse

from bs4 import BeautifulSoup

def get_links(url):
    conn = urllib2.urlopen(url)
    html = conn.read()

    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all('a')

    for tag in links:
        link = tag.get('href',None)
        if link is not None and link.startswith("http"):
            print link
            q.put(link)

def is_empty(q):
    return q.empty()

parser = argparse.ArgumentParser()
parser.add_argument("--url", required=True, help="please specify starting url")
parser.add_argument("--limit", type=int, default=-1, help="please specify a limit (optional)")

args = parser.parse_args()

url = args.url
limit = args.limit

q = Queue.Queue()
q.put(url)

while True and not is_empty(q):
    if limit == 0:
        print "End of the road .."
        exit(0)
    link = q.get()
    tlist = get_links(link)
    limit-=1
    try:
        for link in tlist:
            q.put(link)
            print link
    except TypeError:
        continue
