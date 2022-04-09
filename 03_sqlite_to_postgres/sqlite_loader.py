from typing import Tuple
import db_dataobjects

from sqlite3 import Connection


class SQLiteLoader:

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def load_movies_database(
        self,
        tables: list = [],
        pack_size: int = 500
    ) -> Tuple[str, list]:

        if tables == []:
            tables = self.get_all_table_names()

        for table_name in tables:
            yield from self.load_table(table_name, pack_size)

    def get_all_table_names(self) -> list:
        tables_list = []
        cur = self.conn.cursor()
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        for row in cur.execute(sql_query):
            tables_list.append(row['name'])

        return tables_list

    def load_table(self, table_name: str, pack_size: int) -> Tuple[str, list]:
        DataClass = db_dataobjects.TABLE_TYPES[table_name]

        cur = self.conn.cursor()
        cur.execute(f'SELECT * FROM {table_name};')

        data = []
        while True:
            data.clear()
            result = cur.fetchmany(pack_size)
            if not result:
                return table_name, data

            for row in result:
                kwarg = {}
                for fld in db_dataobjects.get_fields(DataClass):
                    kwarg[fld] = row[fld]
                data.append(DataClass(**kwarg))

            yield table_name, data
