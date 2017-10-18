class BaseQuery:
    def __init__(self, engine, table, columns=None):
        if not isinstance(columns, list):
            raise TypeError("columns must be a list")

        self._table = table
        self._engine = engine
        self._from = table.tablename()
        self._columns = columns or table.columns()
        self._conditions = []
        self._parameters = {}
        self._limit = False

    def get_raw_query(self):
        pass

    def where(self, condition):
        self._parameters.update(condition.get_parameter())
        operation = condition.get_operation(self._engine)
        self._conditions.append(operation)
        return self

    def limit(self, limit):
        if not isinstance(limit, int):
            raise TypeError("Limit must be an integer")

        self._limit = True
        self._parameters.update({'limit_parameter': limit})
        return self

    async def one(self):
        query, params = self.get_raw_query()
        return await self._engine.fetchone(self._table, query, params)

    async def all(self):
        query, params = self.get_raw_query()
        return await self._engine.fetchall(self._table, query, params)

    def __repr__(self):
        query, params = self.get_raw_query()
        return f'<Query query: {query}, params={params}>'


class ResultQuery:
    def __init__(self, table, results):
        self._table = table
        self._results = results
        self._cached_results = {}

    def __iter__(self):
        for pos, result in enumerate(self._results):
            obj = self._table(**result)
            self._cached_results[pos] = obj
            yield obj

    def __getitem__(self, idx):
        if idx in self._cached_results:
            return self._cached_results[idx]

        obj = self._table(**self._results[idx])
        self._cached_results[idx] = obj
        return obj
