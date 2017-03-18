import logging

from aiomysql import create_pool, connect

from sqlchemistry.engine.base import BaseEngine
from sqlchemistry.sql.backends.mysql import MySQLQuery


class MySQLEngine(BaseEngine):
    def __init__(self, *args, **kwargs):
        super(MySQLEngine, self).__init__(*args, **kwargs)

        self._connection = None
        self._pool = None

        self._logger = logging.getLogger("SQLChemistry.engine.mysql")
        self._logger.setLevel(logging.WARNING)

    async def _connect(self):
        self._logger.debug('Connecting...')
        credentials = {
            'host': self._host,
            'port': int(self._port),
            'user': self._user,
            'password': self._pwd,
            'db': self._db,
            'loop': self._loop
        }

        if self._use_pool:
            self._pool = await create_pool(**credentials)

        else:
            self._connection = await connect(**credentials)

    def get_query(self, table, columns=None):
        return MySQLQuery(self, table, columns=columns or table.columns())

    def create_table(self, table):
        def _process_column(column):
            params = {
                'name': column.name,
                'type': column.sql_type,
                'nullable': ' NOT NULL' if column.is_nullable() else '',
                'pk': ' PRIMARY KEY' if column.is_primary_key() else '',
                'inc': ' AUTO_INCREMENT' if column.is_autoincrement() else ''
            }
            return '\t{name} {type}{nullable}{inc}{pk}'.format(**params)

        columns = ',\n'.join(_process_column(c) for c in table.columns())
        corpus = "CREATE TABLE {tablename} (\n{columns}\n);"\
                 .format(tablename=table.tablename(), columns=columns)

        return corpus
