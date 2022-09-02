from dotenv import load_dotenv
from pathlib import Path
import os

load_dotenv()

class FileSettings:
    # Хранилище файлов
    PATH_DIR = Path(os.getenv("PATH_DIR") or "./")

    # Допустимое расширение файлов
    FILE_SUFFIX = os.getenv("FILE_SUFFIX") or ".txt"


class RabbitMQSettings:
    HOST = os.getenv("RABBITMQ_HOST") or "localhost"
    PORT = int(os.getenv("RABBITMQ_PORT")) or 5672
    EXCHANGE = os.getenv("RABBITMQ_EXCHANGE") or "avsoft"


# Используемые в проекте очереди (Queues) в RabbitMQ
class Queues:
    PARSING_QUEUE = os.getenv("RABBITMQ_PARSING_QUEUE") or "Parsing"
    ERROR_QUEUE = os.getenv("RABBITMQ_ERROR_QUEUE") or "Errors"


class MySQLSettings:
    HOST = os.getenv("MYSQL_HOST") or "localhost"
    USER = os.getenv("MYSQL_USER") or ""
    PASSWORD = os.getenv("MYSQL_PASSWORD") or ""
    DATABASE = os.getenv("MYSQL_DATABASE") or ""


class TelegramSettings:
    TOKEN = os.getenv("TELEGRAM_TOKEN") or ""
    CHAT_IDS = [id for id in os.getenv("TELEGRAM_CHAT_IDS").split()]
