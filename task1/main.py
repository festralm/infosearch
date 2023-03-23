import logging
import os
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import urllib.request
from index import Indexer
import furl

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class Crawler:

    def __init__(self, urls=[]):
        self.visited_urls = []
        self.urls_to_visit = urls

    def download_url(self, url):
        return requests.get(url).text

    def get_linked_urls(self, url, html):
        soup = BeautifulSoup(html, 'html.parser')
        for link in soup.find_all('a'):
            path = link.get('href')
            if path and path.startswith('/'):
                path = urljoin(url, path)
            if path is None or not path.startswith('http'):
                continue
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            if url is not None and not url.endswith('.css') and not url.endswith('.js'):
                self.add_url_to_visit(url)

    def run(self, n):
        files_path = 'pages/'
        if not os.path.exists(files_path):
            os.makedirs(files_path)
        url_num = 1
        # create index.txt
        indexer = Indexer("index.txt", overwrite=True)
        while self.urls_to_visit and url_num <= n:
            url = self.urls_to_visit.pop(0)
            # encode to utf8
            url = furl.furl(url).tostr()
            logging.info(f'Crawling №{url_num}: {url}')
            opener = urllib.request.FancyURLopener({})
            try:
                f = opener.open(url)
            except Exception:
                continue
            global content
            try:
                content = f.read()
                with open(files_path + str(url_num) + ".txt", "wb") as binary_file:
                    # Write bytes to file
                    binary_file.write(content)
                    # add entry to index.txt
                    indexer.add(files_path + str(url_num) + ".txt", url)
                try:
                    self.crawl(url)
                except Exception:
                    logging.exception(f'Failed to crawl: {url}')
                finally:
                    if url not in self.visited_urls:
                        url_num = url_num + 1
                        self.visited_urls.append(url)
            except Exception:
                logging.exception(f'Failed to read: {url}')
                self.visited_urls.append(url)


if __name__ == '__main__':
    urls = ['https://shop.tastycoffee.ru/']
    Crawler(urls=urls).run(100)
