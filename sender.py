'''
Ожидает появление файлов в папке и обрабатывает их: при нахождении текстового
файла - передает json сообщение посредством RabbitMQ в очередь: «Parsing», в
сообщении указывает путь до найденного файла; для других типов файлов -
передает аналогичное сообщение в очередь: «Errors».
'''

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from pathlib import Path
import pika
import time
import json


class Watcher:
    def __init__(self,
                 watching_dir,
                 rabbitmq_host=pika.ConnectionParameters("localhost")):
        self.observer = Observer()
        self.watching_dir = watching_dir
        self.rabbitmq_connection = pika.BlockingConnection(rabbitmq_host)

    def run(self):
        event_handler = Handler(self.rabbitmq_connection)
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

    def __init__(self, rabbitmq_connection):
        self.channel = rabbitmq_connection.channel()

    def on_created(self, event):
        if event.is_directory:
            return None

        queue = "Parsing"
        filepath = Path(event.src_path)

        if filepath.suffix != ".txt":
            queue = "Errors"

        message = dict(
            src_path=str(filepath),
            time=time.time())

        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(exchange='',
                                   routing_key="sender",
                                   body=json.dumps(message))


if __name__ == '__main__':
    w = Watcher("./watching")
    w.run()
