'''
Ищет страницы сайта (аналогично поисковому роботу и составлению sitemap.xml) и
записывает содержимое каждой страницы в отдельный файл, в папку Отправителя.
Адрес сайта вводит пользователь.
'''
from settings import FileSettings
from urllib import request, error
from urllib.parse import urljoin
import logging
import re
import sys
import uuid


# Проверка на валидность (временная затычка)
def is_html(url: str):
    not_valid = ('mailto:', '.css', '.js', 'tel:', 'http', 'geo')
    for v in not_valid:
        if v in url:
            return False
    return True


def read_page(url: str):
    try:
        res = request.urlopen(url)
        return res.read().decode()
    except error.HTTPError as http_error:
        logging.error(http_error)
        return str()


# TODO: фильтровать регулярным выражением .css, .js, mailto и tel
def find_links(page):
    href_reg = r'href=[\'"]?([^\'" >]+)'
    return filter(is_html, re.findall(href_reg, page))


# Поиск страниц в глубину
def dfs(current_url, visited=None, volume=None, suffix=""):
    if visited is None:
        visited = set()

    page = read_page(current_url)

    # Запись в файл
    if volume:
        filename = str(uuid.uuid4()) + suffix
        with open(volume.joinpath(filename), 'w') as file:
            file.write(page)

    urls = set(urljoin(current_url, u) for u in find_links(page))
    for url in urls - visited:
        visited.add(url)
        dfs(url, visited, volume, suffix)
    return visited


class Generator:
    def __init__(self,
                 base_url=None,
                 volume=FileSettings.PATH_DIR,
                 suffix=FileSettings.FILE_SUFFIX):
        self.volume = volume
        self.suffix = suffix
        self.base_url = base_url

    def find_links(self, page):
        return set(urljoin(self.base_url, a) for a in find_links(page))

    def run(self):
        if not self.base_url:
            self.base_url = input("URL: ")
        logging.info(f'Searching in {self.base_url}')
        dfs(self.base_url, volume=self.volume, suffix=self.suffix)


if __name__ == "__main__":
    base_url = None
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    w = Generator(base_url)
    w.run()
