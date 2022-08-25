'''
Обрабатывает данные таблицы в MySQL: когда слово встретилось N раз и более,
удаляет запись и создает файл, содержащий 2 строки: само слово и имена файлов,
содержащих данное слово. N - константа с произвольным значением.
'''
from database import MySQLClientMixin
from time import sleep


class Reader(MySQLClientMixin):
    def __init__(self, count=1, hold_time=10):
        self.words_cound = count
        self.hold_time = hold_time

    # TODO: Создание файлов
    def remove_writes(self):
        with open("database/queries/remove_writes.sql") as f:
            query = f.read() % self.words_cound
            self.send_query(query)

    # TODO: Watchdod?
    def run(self):
        print(f'[*] Reader has started. To exit press CTRL + C')
        try:
            while True:
                self.remove_writes()
                sleep(self.hold_time)
        except KeyboardInterrupt:
            pass


if __name__ == "__main__":
    w = Reader(1)
