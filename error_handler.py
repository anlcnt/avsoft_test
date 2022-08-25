'''
Оповещает посредством электронной почты/Telegram/SIEM/SOAR, в случае
получения сообщения из очереди: «Errors». В случае ошибки отправки оповещения,
оповещение должно произойти ПОЗДНЕЕ.
'''

from rabbitmq import Subscriber
from datetime import datetime
from settings import RabbitMQSettings, TelegramSettings, Queues
from threading import Timer
import requests
import json


class ErrorHandler(Subscriber):
    def __init__(self,
                 rabbitmq_config=RabbitMQSettings,
                 tg_config=TelegramSettings,
                 queue=Queues.ERROR_QUEUE):
        super(ErrorHandler, self).__init__(rabbitmq_config, queue)
        if tg_config.TOKEN:
            self.tg = TelegramSender(token=tg_config.TOKEN,
                                     chats=tg_config.CHAT_IDS)

    # TODO: Большое количество сообщений может завалить количеством потоков
    # TODO: Добавить отправку по почте, SIEM, SOAR
    def send(self, data: dict):
        print("trying send")
        if self.tg.alive:
            dt_msg = datetime.utcfromtimestamp(
                data['time']).strftime('%Y-%m-%d %H:%M:%S')
            src_path = data['src_path']
            msg = (f"{dt_msg}: Error on {src_path}")
            self.tg.send_to_users(msg)
        else:
            t = Timer(3, self.send, kwargs={"data": data})
            t.start()

    def on_message_callback(self, channel, method, properties, body):
        self.send(json.loads(body))


class TelegramSender:
    def __init__(self,
                 token=TelegramSettings.TOKEN,
                 chats=TelegramSettings.CHAT_IDS):
        self._token = token
        self._chats = chats

    @property
    def token(self):
        return self._token

    @property
    def chats(self):
        return self._chats

    def get(self, method, params={}):
        url = f"https://api.telegram.org/bot{self._token}/{method}"
        return requests.get(url, params=params)

    def alive(self):
        response = self.get("getMe")
        if response.status_code == 200:
            return response.json()['ok']
        return False

    def _send(self, chat_id, message, parse_mode="Markdown"):
        response = self.get("sendMessage", params={
            "chat_id": chat_id,
            "parse_mode": parse_mode,
            "text": message
        })
        return response.json()

    def send_to_users(self, message, parse_mode="Markdown"):
        for chat_id in self.chats:
            self._send(chat_id, message, parse_mode)


if __name__ == '__main__':
    w = ErrorHandler()
    w.run()
