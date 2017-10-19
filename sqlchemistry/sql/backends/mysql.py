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
        if self._conditions:
            conditions = '\nAND '.join(self._conditions)
            return 'WHERE ({})'.format(conditions)

        return ''

    def _apply_limit(self):
        if not self._limit:
            return ''

        return f'LIMIT %(limit_parameter)s'

    def _apply_joins(self):
        sql = ''

        joins = [
            ('inner', 'INNER JOIN'),
            ('left', 'LEFT JOIN'),
            ('right', 'RIGHT JOIN')
        ]

        for join_type, join_sql in joins:
            for table, stmt_on in self._joins[join_type]:
                stmt_on = f'ON {stmt_on}' if stmt_on is not None else ''
                sql += f'{join_sql} {table.tablename()} {stmt_on} '

        return sql

    def get_raw_query(self):
        sql = self._apply_select()
        joins = self._apply_joins()
        wheres = self._apply_wheres()
        limit = self._apply_limit()
        return [f'{sql} {joins} {wheres} {limit}', self._parameters]
