import logging

from aiomysql import create_pool, connect

from sqlchemistry.engine.base import BaseEngine
from sqlchemistry.sql.mysql import MySQLQuery


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
        return MySQLQuery(table, columns=columns)
