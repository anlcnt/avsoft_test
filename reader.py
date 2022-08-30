'''
Обрабатывает данные таблицы в MySQL: когда слово встретилось N раз и более,
удаляет запись и создает файл, содержащий 2 строки: само слово и имена файлов,
содержащих данное слово. N - константа с произвольным значением.
'''
from settings import FileSettings
from database import MySQLClientMixin
from time import sleep
from pathlib import Path


# Генератор, определяющий наличие слова в файле
def get_words(filesdir: Path, word: str, suffix=".txt"):
    fpaths = (fp for fp in filesdir.iterdir() if fp.suffix == suffix)
    for fpath in fpaths:
        with open(fpath) as file:
            # TODO: Здесь можно использовать какой-нибудь алгоритм поиска
            txt = file.read()
            # TODO: Поиск слов регулярным выражением
            if word in txt.lower():
                yield fpath.name


class Reader(MySQLClientMixin):
    def __init__(self,
                 volume=FileSettings.PATH_DIR,
                 count=1,
                 hold_time=10):
        self.count = count
        self.volume = volume
        self.hold_time = hold_time

    # TODO: Определение, куда записывать файл
    def remove_writes(self, output="out.txt"):
        sel_q = f"SELECT word FROM words WHERE count > {self.count};"
        del_q = f"DELETE FROM words WHERE count > {self.count};"
        records = self.select(sel_q)
        self.insert(del_q)

        '''
        В принципе, этот метод можно было сделать иначе, создав таблицу в базе
        данных с файлами. В таком случае, будут проблемы с синхронизацией, да и
        задание не предусматривает собой такой способ
        '''
        # TODO: Запись файла
        with open(output, 'a') as f:
            for record in records:
                word, = record
                rec = f"{word}:{', '.join(get_words(self.volume, word))};\n"
                f.write(rec)

    # TODO: Watchdod?
    def run(self):
        print(f'Reader has started. To exit press CTRL + C')
        try:
            while True:
                self.remove_writes()
                sleep(self.hold_time)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    w = Reader(FileSettings.PATH_DIR, 2)
    w.run()
