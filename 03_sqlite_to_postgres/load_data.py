import sqlite3
import psycopg2
import os

from dotenv import load_dotenv
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor
from sqlite_loader import SQLiteLoader
from postgres_saver import PostgresSaver

from contextlib import contextmanager


@contextmanager
def sqlite_context(db_path: str):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def pg_context(**dsl):
    conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        yield conn
    finally:
        conn.close()


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres"""
    postgres_saver = PostgresSaver(pg_conn)
    sqlite_loader = SQLiteLoader(connection)

    pack_size =int(os.environ.get('PACK_SIZE'))
    for table_name, data in sqlite_loader.load_movies_database(pack_size=pack_size):
        if data:
            postgres_saver.save_data(table_name, data)


if __name__ == '__main__':

    load_dotenv()

    dsl = {
        'dbname': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),
        }

    sqlite_path = os.environ.get('DB_SQLITE_PATH')
    with sqlite_context(sqlite_path) as sqlite_conn,\
            pg_context(**dsl) as pg_conn:

        load_from_sqlite(sqlite_conn, pg_conn)
