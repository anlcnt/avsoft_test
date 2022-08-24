'''
Обрабатывает сообщения очереди: «Parsing»: извлекает слова из текста и
записывает их в таблицу MySQL с указанием количества вхождений в тексте
(для каждого слова, соответственно). В качестве разделителя слов используются
все не буквенные символы. Если слово уже есть в таблице, то увеличивает
количество вхождений на соответствующее число.
'''

from rabbitmq import queues as q, Worker
import re
import json
import logging


# Регулярное выражение для парсинга
# TODO: Нормальный парсинг
PARSING_REGULAR = r"a-zA-Z0-9А-Яа-я()"


class Parser(Worker):
    def __init__(self,
                 amqp_con_parameters: dict,
                 queue=q.PARSING_QUEUE):
        super(Parser, self).__init__(amqp_con_parameters)
        self._queue = queue

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        logging.info(f"Incoming message from {binding_key}")

        try:
            message = json.loads(body)
            path = message["src_path"]
            self.parse(path)
        except json.decoder.JSONDecodeError:
            logging.error(f"{body} has not a JSON")
        except Exception as e:
            logging.error(e)

    def parse(self, src_path: str):
        with open(src_path) as file:
            data = dict()
            for line in file:
                line = line.lower()
                words = re.sub(PARSING_REGULAR, "", line).split()
                for word in words:
                    if word not in data:
                        data[word] = 0
                    data[word] += 1
            print(data)

    def run(self):
        super(Parser, self).run()
        self.subscribe(routing_key=self._queue, queue=self._queue)


if __name__ == "__main__":
    p = Parser({"host": "localhost", "port": 5672, "exchange": "test"})
    p.run()
