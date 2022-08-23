from abc import ABC
import pika
import logging


# Класс для взаимодействия с RabbitMQ
class Worker(ABC):
    def __init__(self, con_config: dict):
        self.connection = Worker._create_connection(**con_config)

    def __del__(self):
        self.connection.close()
        logging.info("Connection closed")

    @staticmethod
    def _create_connection(host="localhost", port=5672, *args, **kwargs):
        # TODO: Передача полного списка параметров RabbitMQ
        params = pika.ConnectionParameters(host, port)
        return pika.BlockingConnection(params)

    def run(self):
        logging.info(f"{type(self).__name__} was started")
