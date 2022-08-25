'''
Оповещает посредством электронной почты/Telegram/SIEM/SOAR, в случае
получения сообщения из очереди: «Errors». В случае ошибки отправки оповещения,
оповещение должно произойти ПОЗДНЕЕ.
'''

from rabbitmq import Subscriber
from datetime import datetime
from settings import RabbitMQSettings, TelegramSettings, Queues
import requests
import json


class ErrorHandler(Subscriber):
    def __init__(self,
                 rabbitmq_config=RabbitMQSettings,
                 tg_config=TelegramSettings,
                 queue=Queues.ERROR_QUEUE):
        super(ErrorHandler, self).__init__(rabbitmq_config, queue)
        self.tg_config = TelegramSettings

    # TODO: Планировщик
    # TODO: Добавить отправку по почте, SIEM, SOAR
    def send(self, data: dict):
        if tg_health_check(self.tg_config.TOKEN):
            dt_msg = datetime.utcfromtimestamp(
                data['time']).strftime('%Y-%m-%d %H:%M:%S')
            src_path = data['src_path']
            msg = (f"{dt_msg}: Error on {src_path}")
            send_to_telegram(self.tg_config.TOKEN, self.config["chat_id"], msg)

    def on_message_callback(self, channel, method, properties, body):
        self.send(json.loads(body))


# Отправка сообщения по Telegram
def send_to_telegram(token: str,
                     chat_id: int,
                     message: str,
                     parse_mode="Markdown"):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    response = requests.get(url, params={
        "chat_id": chat_id,
        "parse_mode": parse_mode,
        "text": message
    })
    return response.json()


def tg_health_check(token: str):
    url = f'https://api.telegram.org/bot{token}/getMe'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()['ok']
    return False


# Массовая рассылка по Telegram
def bulk_send_to_telegram(token: str,
                          chats_id: list,
                          message: str,
                          parse_mode="Markdown"):
    for id in chats_id:
        send_to_telegram(token, id, message, parse_mode)


if __name__ == '__main__':
    w = ErrorHandler()
    w.run()
