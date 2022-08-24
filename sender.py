'''
Ожидает появление файлов в папке и обрабатывает их: при нахождении текстового
файла - передает json сообщение посредством RabbitMQ в очередь: «Parsing», в
сообщении указывает путь до найденного файла; для других типов файлов -
передает аналогичное сообщение в очередь: «Errors».
'''

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from rabbitmq import queues as q, Publisher
import time


class Watcher(Publisher):
    def __init__(self,
                 watching_dir: str,
                 amqp_con_parameters: dict):
        super(Watcher, self).__init__(amqp_con_parameters)
        self.observer = Observer()
        self.watching_dir = watching_dir

    def run(self):
        super(Watcher, self).run()
        event_handler = Handler(self.publish)

        self.observer.schedule(
            event_handler, self.watching_dir, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except Exception as e:
            self.observer.stop()
            print(e)

        self.observer.join()


class Handler(FileSystemEventHandler):
    def __init__(self, on_send_callback):
        self.on_send_callback = on_send_callback

    def on_created(self, event):
        if event.is_directory:
            return None

        filepath = Path(event.src_path)
        queue = q.PARSING_QUEUE if filepath.suffix == ".txt" else q.ERROR_QUEUE
        data = dict(
            src_path=str(filepath),
            time=time.time())

        self.on_send_callback(queue, data)


if __name__ == '__main__':
    w = Watcher("./watching", {"host": "localhost", "exchange": "test"})
    w.run()
