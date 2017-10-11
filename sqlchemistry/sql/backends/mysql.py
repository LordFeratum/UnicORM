from sqlchemistry.sql.base import BaseQuery


class MySQLQuery(BaseQuery):
    def __init__(self, engine, table, columns=None):
        super(MySQLQuery, self).__init__(engine, table, columns=columns)

    def _apply_select(self):
        columns = ', '.join('{}.`{}`'.format(self._from, c.name)
                            for c in self._columns)

        return 'SELECT {columns} FROM {table}'.format(columns=columns,
                                                      table=self._from)

    def _apply_wheres(self):
        conditions = '\nAND '.join(self._conditions)
        return 'WHERE {}'.format(conditions)

    def get_raw_query(self):
        sql = self._apply_select()
        wheres = self._apply_wheres()
        return ['{}\n{}'.format(sql, wheres), self._parameters]
