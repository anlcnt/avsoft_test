'''
Ищет страницы сайта (аналогично поисковому роботу и составлению sitemap.xml) и
записывает содержимое каждой страницы в отдельный файл, в папку Отправителя.
Адрес сайта вводит пользователь.
'''
from settings import PATH_DIR
from urllib import request, error
from urllib.parse import urljoin
from pathlib import Path
import re
import sys


# Проверка на валидность (временная затычка)
def is_html(url):
    not_valid = ('mailto:', '.css', '.js', 'tel:', 'http', 'geo')
    for v in not_valid:
        if v in url:
            return False
    return True


def read_page(url):
    try:
        res = request.urlopen(url)
        return res.read().decode()
    except error.HTTPError:
        return ""


# TODO: фильтровать регулярным выражением .css, .js, mailto и tel
def find_links(page: str):
    href_reg = r'href=[\'"]?([^\'" >]+)'
    return filter(is_html, re.findall(href_reg, page))


def dfs(base_url, url=None, visited=None):
    if visited is None:
        visited = set()
    if url is None:
        url = base_url

    def join(u1, u2):
        return urljoin(base_url, u2) if u2[0] == '/' else urljoin(u1, u2)

    page = read_page(url)
    urls = set(join(url, u) for u in find_links(page))
    for current_url in urls - visited:
        visited.add(current_url)
        dfs(base_url, current_url, visited)
    return visited


class Generator:
    def __init__(self, volume=PATH_DIR, base_url=None):
        self.volume = volume
        self.base_url = base_url
        self.urls = set()

    def find_links(self, page):
        return set(urljoin(self.base_url, a) for a in find_links(page))

    def run(self):
        if not self.base_url:
            self.base_url = input("URL: ")
        base_page = read_page(self.base_url)
        self.urls = self.find_links(base_page)
        n_urls = set()
        while self.urls != n_urls:
            n_urls = set(self.urls)
            for url in n_urls:
                try:
                    page = read_page(url)
                    print(url)
                except Exception:
                    print('ERROR', url)
                    continue
                # TODO: Запись в файл
                self.urls.update(self.find_links(page))


# if __name__ == "__main__":
#     base_url = None
#     if len(sys.argv) > 1:
#         base_url = sys.argv[1]
#     w = Generator(base_url=base_url)
#     w.run()

if __name__ == "__main__":
    base_url = None
    if len(sys.argv) > 1:
        base_url = sys.argv[1]
    print(dfs(base_url))
