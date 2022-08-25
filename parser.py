'''
Обрабатывает сообщения очереди: «Parsing»: извлекает слова из текста и
записывает их в таблицу MySQL с указанием количества вхождений в тексте
(для каждого слова, соответственно). В качестве разделителя слов используются
все не буквенные символы. Если слово уже есть в таблице, то увеличивает
количество вхождений на соответствующее число.
'''

from rabbitmq import Subscriber
from settings import RabbitMQSettings, Queues
from database import MySQLClientMixin
import re
import json
import logging


# Регулярное выражение для парсинга
REG_CHAR = r"[^a-zA-Zа-яА-ЯёЁ]"


class Parser(Subscriber, MySQLClientMixin):
    def __init__(self,
                 rabbitmq_config=RabbitMQSettings,
                 queue=Queues.PARSING_QUEUE):
        super(Parser, self).__init__(rabbitmq_config, queue)

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        logging.info(f"Incoming message from {binding_key}")

        try:
            message = json.loads(body)
            path = message["src_path"]
            self.parse(path)
        except json.decoder.JSONDecodeError:
            logging.error(f"{body} has not a JSON")
        # TODO: Разобраться с этим недоразумением
        except Exception as e:
            logging.error(e)

    # Заносим данные в базу
    def push_data(self, data):
        with open("database/queries/insert_or_update.sql") as f:
            query = f.read() % ",".join([str(v) for v in data.items()])
            self.insert(query)

    def parse(self, src_path: str):
        with open(src_path) as file:
            data = dict()
            for line in file:
                line = line.lower()
                words = [word for word in re.split(REG_CHAR, line) if word]
                for word in words:
                    if word not in data:
                        data[word] = 0
                    data[word] += 1
        self.push_data(data)


if __name__ == "__main__":
    p = Parser()
    p.run()
