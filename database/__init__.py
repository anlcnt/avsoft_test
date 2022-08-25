from mysql.connector import connect, Error
from settings import MySQLSettings
import logging


def exception_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Error as e:
            logging.error(e)
    return wrapper


# Не стал использовать ORM по причине простоты базы
class MySQLClientMixin:
    # TODO: Создание базы данных при её отсутствии
    def connect(self):
        return connect(
            host=MySQLSettings.HOST,
            user=MySQLSettings.USER,
            password=MySQLSettings.PASSWORD,
            database=MySQLSettings.DATABASE,
        )

    @exception_handler
    def select(self, query):
        with self.connect() as connection:
            with connection.cursor() as cur:
                cur.execute(query)
                return cur.fetchall()

    @exception_handler
    def insert(self, query):
        with self.connect() as connection:
            with connection.cursor() as cur:
                cur.execute(query)
                connection.commit()
