from rabbitmq import queues as q
from abc import ABC
import pika
import json
import logging


# Класс для взаимодействия с RabbitMQ
class Worker(ABC):
    def __init__(self, config: dict):
        self.config = config

    def __del__(self):
        pass

    @property
    def exchange(self):
        return self.config["exchange"] or ""

    @staticmethod
    def _create_connection(host="localhost", port=5672, *args, **kwargs):
        # TODO: Передача полного списка параметров RabbitMQ
        params = pika.ConnectionParameters(host=host,
                                           port=port)
        return pika.BlockingConnection(params)

    @staticmethod
    def _create_channel(connection, exchange="", *args, **kwargs):
        # TODO: Отлов ошибки при создании канала
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange,
                                 exchange_type="topic")
        return channel

    def run(self):
        logging.info(f"{type(self).__name__} was started")


# Издатель
class Publisher(Worker):
    def __init__(self, config: dict):
        super(Publisher, self).__init__(config)
        self.config = config

    # Публикация JSON в очередь
    def publish(self, routing_key: str, data: dict):
        connection = Worker._create_connection(**self.config)
        # TODO: Отлов ошибки при создании json'а
        message = json.dumps(data)
        channel = Worker._create_channel(connection, self.exchange)
        channel.basic_publish(exchange=self.exchange,
                              routing_key=routing_key,
                              body=message)
        logging.info(f"{type(self).__name__} sends {message} to {routing_key}")
        connection.close()


# Подписчик
class Subscriber(Worker):
    def __init__(self, config: dict, queue=q.PARSING_QUEUE):
        super(Subscriber, self).__init__(config)
        self.queue = queue

    def on_message_callback(self, channel, method, properties, body):
        binding_key = method.routing_key
        logging.info(f"received new message for - {binding_key} {body}")

    # Подписка на очередь
    def subscribe(self, routing_key: str, queue: str):
        connection = Worker._create_connection(**self.config)
        channel = Worker._create_channel(connection=connection,
                                         exchange=self.exchange)
        channel.queue_declare(queue=queue)
        channel.queue_bind(queue=queue,
                           exchange=self.exchange,
                           routing_key=routing_key)
        channel.basic_consume(queue=queue,
                              on_message_callback=self.on_message_callback,
                              auto_ack=True)

        # TODO: Что-то сделать с этим
        print(f'[*] Waiting for data for {queue}. To exit press CTRL + C')
        try:
            channel.start_consuming()
        except KeyboardInterrupt:
            channel.stop_consuming()
            connection.close()
            logging.info("Connection closed")

    def run(self):
        super(Subscriber, self).run()
        self.subscribe(routing_key=self.queue, queue=self.queue)
