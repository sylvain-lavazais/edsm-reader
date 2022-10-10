from typing import List, Any

import psycopg2
from psycopg2.extras import DictCursor


class Database:
    db_host: str
    db_port: str
    db_user: str
    db_name: str
    db_password: str

    def __init__(self, db_host: str, db_port: str, db_user: str, db_name: str, db_password: str):
        self.db_host = db_host
        self.db_port = db_port
        self.db_user = db_user
        self.db_name = db_name
        self.db_pass = db_password

    def __db_connection(self):
        try:
            params = {
                'database': self.db_name,
                'user': self.db_user,
                'password': self.db_pass,
                'host': self.db_host,
                'port': self.db_port
            }
            return psycopg2.connect(**params)
        except (Exception, psycopg2.DatabaseError) as error:
            print(f'Error occur on connection to database - {error}')

    def exec_db_read(self, query: str, param: dict = None) -> List[dict]:
        try:
            with self.__db_connection() as connection:
                with connection.cursor(cursor_factory=DictCursor) as cursor:
                    cursor.execute(query, param)
                    return cursor.fetchall()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f'Error occur on read - {error}')

    def exec_db_write(self, query: str, params: dict) -> None:
        try:
            with self.__db_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(query, params)
                    query_str = str(cursor.query, 'utf-8').replace('\n', '')
                    print(f'executing query [{query_str}]')
                    connection.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print(f'Error occur on write - {error}')
            connection.rollback()
