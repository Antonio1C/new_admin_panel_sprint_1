from db_dataobjects import TABLE_TYPES, FIELD_MATCHING, get_fields

from psycopg2.extensions import connection


class PostgresSaver:

    PACK_SIZE = 200

    def __init__(self, conn: connection) -> None:
        self.conn = conn

    def save_all_data(self, data: dict) -> None:
        for table_name, table_data in data.items():
            self.__update_table(table_name, table_data)

    def __update_table(self, table_name: str, table_data: list) -> None:
        cur = self.conn.cursor()
        pack_size = PostgresSaver.PACK_SIZE

        DataClass = TABLE_TYPES[table_name]
        t_fields = get_fields(DataClass)

        # some fields has enother name in the postgres's movies_database
        pt_fields = []
        for fld in t_fields:
            pt_fields.append(FIELD_MATCHING.get(fld, fld))

        insert_header = f'INSERT INTO content.{table_name} (' + \
            ', '.join(pt_fields) + ')\nVALUES'

        sql_query = insert_header
        sep = ''
        for i in range(len(table_data)):
            if i != 0 and i % pack_size == 0:
                sql_query += ('\nON CONFLICT (id) DO NOTHING;')
                cur.execute(sql_query)
                sql_query = insert_header
                sep = ''

            values = []
            for fld in t_fields:
                value = str(getattr(table_data[i], fld)).replace('\'', '\'\'')
                value = 'NULL' if value == 'None' else '\'' + value + '\''
                values.append(value)

            sql_query += (f'{sep}\n(' + ', '.join(values) + ')')

            sep = ',' if sep == '' else sep

        if i != 0:
            sql_query += ('\nON CONFLICT (id) DO NOTHING;')
            cur.execute(sql_query)
