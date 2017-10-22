class Session:
    def __init__(self, engine):
        self._engine = engine

    async def connect(self):
        await self._engine.connect()

    def query(self, table, columns=None):
        return self._engine.get_query(table, columns=columns)

    async def commit(self):
        await self._engine.commit()

    async def execute(self, query, params=None, echo=False):
        return await self._engine.execute(query, params, echo)

    async def create_table(self, table, echo=False):
        await self._engine.create_table(table, False, echo)

    async def create_table_if_not_exists(self, table, echo=False):
        await self._engine.create_table(table, True, echo)

    async def insert(self, entity):
        return await self._engine.insert(entity)

    async def delete(self, obj):
        return await self._engine.delete(obj)
