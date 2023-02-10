import logging
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
import urllib.request

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
            yield path

    def add_url_to_visit(self, url):
        if url not in self.visited_urls and url not in self.urls_to_visit:
            self.urls_to_visit.append(url)

    def crawl(self, url):
        html = self.download_url(url)
        for url in self.get_linked_urls(url, html):
            if url is not None and not url.endswith('.css') and not url.endswith('.js'):
                self.add_url_to_visit(url)

    def run(self):
        files_path = 'pages/'
        page_num = 1
        while self.urls_to_visit:
            url = self.urls_to_visit.pop(0)
            logging.info(f'Crawling: {url}')
            opener = urllib.request.FancyURLopener({})
            f = opener.open(url)
            content = f.read()
            with open(files_path + str(page_num) + ".txt", "wb") as binary_file:
                # Write bytes to file
                binary_file.write(content)
            try:
                self.crawl(url)
            except Exception:
                logging.exception(f'Failed to crawl: {url}')
            finally:
                page_num = page_num + 1
                self.visited_urls.append(url)


if __name__ == '__main__':
    urls = ['https://crawler-test.com/']
    Crawler(urls=urls).run()
