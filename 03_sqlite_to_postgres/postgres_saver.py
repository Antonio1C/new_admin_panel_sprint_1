from db_dataobjects import TABLE_TYPES, FIELD_MATCHING, get_fields, get_fields_types

from psycopg2.extensions import connection


class PostgresSaver:

    def __init__(self, conn: connection) -> None:
        self.conn = conn

    def save_data(self, table_name: str, data: list) -> None:
        cur = self.conn.cursor()

        DataClass = TABLE_TYPES[table_name]
        t_fields = get_fields(DataClass)
        t_fields_types = get_fields_types(DataClass)

        # some fields has enother name in the postgres's movies_database
        pt_fields = []
        for fld in t_fields:
            pt_fields.append(FIELD_MATCHING.get(fld, fld))

        values = [f'${i}' for i in range(1, len(pt_fields) + 1)]

        sql_query = 'PREPARE temp_table_insert(' + ', '.join(t_fields_types) + ')' + \
            f' AS \n\tINSERT INTO content.{table_name} (' + ', '.join(pt_fields) + \
            ') VALUES (' + ', '.join(values) + ')\n\tON CONFLICT (id) DO NOTHING;'

        cur.execute(sql_query)
        self.conn.commit()

        sql_query = 'BEGIN;\n'
        for i in range(len(data)):
            values = []
            for fld in t_fields:
                value = str(getattr(data[i], fld)).replace('\'', '\'\'')
                value = 'NULL' if value == 'None' else '\'' + value + '\''
                values.append(value)

            sql_query += ('EXECUTE temp_table_insert(' + ', '.join(values) + ');\n')

        sql_query += 'COMMIT;'

        self.conn.autocommit = False
        cur.execute(sql_query)
        self.conn.commit()
        self.conn.autocommit = True

        sql_query = 'DEALLOCATE temp_table_insert;'
        cur.execute(sql_query)
