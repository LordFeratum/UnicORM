from asyncio import get_event_loop

from dsnparse import parse as parse_dsn


class BaseEngine:
    def __init__(self, dsn=None, host=None, port=None, user=None, pwd=None,
                 database=None, use_pool=True, min_size=1, max_size=10,
                 autocommit=True, loop=None):

        if dsn:
            parsed = parse_dsn(dsn)
            self._host = parsed.host
            self._port = parsed.port
            self._user = parsed.username
            self._pwd = parsed.password

            try:
                self._db = parsed.paths[0]

            except IndexError as e:
                raise KeyError("Database was not specified in the DSN") from e

        else:
            self._host = host
            self._port = port
            self._user = user
            self._pwd = pwd
            self._db = database

        self._connection = None
        self._pool = None
        self._autocommit = autocommit
        self._use_pool = use_pool
        self._minsize = min_size
        self._maxsize = max_size
        self._loop = loop or get_event_loop()

    async def connect(self):
        try:
            return await self._connect()

        except ConnectionError as e:
            params = dict(host=self._host, port=self._port, db=self._db,
                          user=self._user, pwd=self._pwd)
            msg = "Could not connect to {user}:{pwd}@{host}:{port}/{db}"
            raise ConnectionError(msg.format(**params)) from e

    async def insert(self, entity):
        pass
