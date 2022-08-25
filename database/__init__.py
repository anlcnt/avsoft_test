from mysql.connector import connect, Error
from settings import MySQLSettings
import logging


class MySQLClientMixin:
    # TODO: Создание базы данных при её отсутствии
    def connect(self):
        return connect(
            host=MySQLSettings.HOST,
            user=MySQLSettings.USER,
            password=MySQLSettings.PASSWORD,
            database=MySQLSettings.DATABASE,
        )

    def send_query(self, query):
        try:
            with self.connect() as connection:
                with connection.cursor() as cur:
                    cur.execute(query)
        except Error as e:
            logging.error(e)
