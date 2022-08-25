'''
Обрабатывает данные таблицы в MySQL: когда слово встретилось N раз и более,
удаляет запись и создает файл, содержащий 2 строки: само слово и имена файлов,
содержащих данное слово. N - константа с произвольным значением.
'''
from settings import PATH_DIR
from database import MySQLClientMixin
from time import sleep


class Reader(MySQLClientMixin):
    def __init__(self, count=1, watch_dir=PATH_DIR, hold_time=10):
        self.count = count
        self.dir = watch_dir
        self.hold_time = hold_time

    # TODO: Определение, куда записывать файл
    def remove_writes(self):
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
        for record in records:
            word, = record

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
    w = Reader(10)
    w.run()
