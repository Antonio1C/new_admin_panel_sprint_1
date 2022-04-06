import db_dataobjects

from sqlite3 import Connection


class SQLiteLoader:

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def load_movies_database(self, tables: list = []) -> dict:

        if tables == []:
            tables = self.get_all_table_names()

        data = {}
        for table_name in tables:
            data[table_name] = []
            self.load_table(data[table_name], table_name)

        return data

    def get_all_table_names(self) -> list:
        tables_list = []
        cur = self.conn.cursor()
        sql_query = "SELECT name FROM sqlite_master WHERE type='table';"
        for row in cur.execute(sql_query):
            tables_list.append(row['name'])

        return tables_list

    def load_table(self, data_list: list, table_name: str) -> None:
        cur = self.conn.cursor()
        sql_query = f'SELECT * FROM {table_name};'
        DataClass = db_dataobjects.TABLE_TYPES[table_name]
        for row in cur.execute(sql_query):
            kwarg = {}
            for fld in db_dataobjects.get_fields(DataClass):
                kwarg[fld] = row[fld]
            data_list.append(DataClass(**kwarg))
