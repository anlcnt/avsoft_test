'''
Ищет страницы сайта (аналогично поисковому роботу и составлению sitemap.xml) и
записывает содержимое каждой страницы в отдельный файл, в папку Отправителя.
Адрес сайта вводит пользователь.
'''
from settings import PATH_DIR
from urllib import parse, request, error
import re
import sys


# Проверка на валидность (временная затычка)
def is_html(url):
    not_valid = ('mailto:', '.css', '.js', 'tel:', 'http')
    for v in not_valid:
        if v in url:
            return False
    return True


def read_page(url):
    return request.urlopen(url).read().decode()


# TODO: фильтровать регулярным выражением .css, .js, mailto и tel
def find_links(page: str):
    href_reg = r'href=[\'"]?([^\'" >]+)'
    return set(filter(is_html, re.findall(href_reg, page)))


# TODO: Поиск в глубину
def dfs(urls, visited=None):
    if visited is None:
        visited = set()

    for url in urls - visited:
        dfs(urls, visited)

    return visited


class Generator:
    def __init__(self, volume=PATH_DIR, base_url=None):
        self.volume = volume
        self.base_url = base_url
        self.urls = set()

    def find_links(self, page):
        return set(parse.urljoin(self.base_url, a) for a in find_links(page))

    def run(self):
        if not self.base_url:
            self.base_url = input("URL: ")
        base_page = read_page(self.base_url)
        self.urls = self.find_links(base_page)
        n_urls = set()
        while self.urls != n_urls:
            # n_urls = set(self.urls)
            n_urls = find_links()
            for url in n_urls:
                try:
                    page = read_page(url)
                    print(url)
                except Exception:
                    print('ERROR', url)
                    continue
                self.urls.update(self.find_links(page))


if __name__ == "__main__":
    base_url = None
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    w = Generator(base_url=base_url)
    w.run()
