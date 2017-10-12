import logging

from aiomysql import create_pool, connect

from sqlchemistry.engine.base import BaseEngine
from sqlchemistry.sql.backends.mysql import MySQLQuery


class MySQLEngine(BaseEngine):
    EQUALS = '='

    def __init__(self, *args, **kwargs):
        self._logger = logging.getLogger()
        self._logger.setLevel(logging.DEBUG)
        super(MySQLEngine, self).__init__(*args, **kwargs)

    async def _connect(self):
        self._logger.debug('Connecting...')
        credentials = {
            'host': self._host,
            'port': int(self._port or '3306'),
            'user': self._user,
            'password': self._pwd,
            'db': self._db,
            'loop': self._loop
        }

        if self._use_pool:
            self._pool = await create_pool(**credentials)

        else:
            self._connection = await connect(**credentials)

    def get_dbapi_identifier(self, identifier):
        return '%({})s'.format(identifier)

    def get_query(self, table, columns=None):
        return MySQLQuery(self, table, columns=columns or table.columns())

    async def execute(self, query, params, echo=False):
        async with self._connection.cursor() as cur:
            if echo:
                print(cur.mogrify(query, params))
            return await cur.execute(query, params)

    async def create_table(self, table, echo):
        def _process_column(column):
            params = {
                'name': column.name,
                'type': column.sql_type,
                'nullable': ' NOT NULL' if column.is_nullable() else '',
                'pk': ' PRIMARY KEY' if column.is_primary_key() else '',
                'inc': ' AUTO_INCREMENT' if column.is_autoincrement() else ''
            }
            return '\t{name} {type}{nullable}{inc}{pk}'.format(**params)

        table._init_columns()
        columns = ',\n'.join(_process_column(c) for c in table.columns())
        corpus = "CREATE TABLE {tablename} (\n{columns}\n);"\
                 .format(tablename=table.tablename(), columns=columns)

        return await self.execute(corpus, None, echo=echo)
