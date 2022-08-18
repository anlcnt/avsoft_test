from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import json
import os


class Watcher:
    def __init__(self, watching_dir):
        self.observer = Observer()
        self.watching_dir = watching_dir

    def run(self):
        event_handler = Handler()
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

    @staticmethod
    def send_message(path, query_name="Parsing"):
        message = dict(
            src_path=path,
            time=time.time())
        if query_name == "Errors":
            message["err"] = True
        print(json.dumps(message))

    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None

        file_extension = os.path.splitext(event.src_path)[-1]

        if file_extension == ".txt":
            Handler.send_message(event.src_path)
        else:
            Handler.send_message(event.src_path, "Errors")


if __name__ == '__main__':
    w = Watcher("./watching")
    w.run()
