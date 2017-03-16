from sqlchemistry.sql.base import BaseQuery


class MySQLQuery(BaseQuery):
    def __init__(self, table, columns=None):
        super(MySQLQuery, self).__init__(table, columns=columns)

    def get_raw_query(self):
        columns = ','.join('{}.{}'.format(self._from, c.get_name())
                           for c in self._columns)

        sql = 'SELECT {columns} FROM {table}'.format(columns=columns,
                                                     table=self._from)
        return sql
