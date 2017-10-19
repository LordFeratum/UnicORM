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
        self._joins = {
            'inner': [],
            'left': [],
            'right': []
        }

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

    def inner_join(self, table, on=None):
        if on is not None:
            on = on.get_unproccesed_operation(self._engine)

        self._joins['inner'].append((table, on))
        return self

    def left_join(self, table, on=None):
        if on is not None:
            on = on.get_unproccesed_operation(self._engine)

        self._joins['left'].append((table, on))
        return self

    def right_join(self, table, on=None):
        if on is not None:
            on = on.get_unproccesed_operation(self._engine)

        self._joins['right'].append((table, on))
        return self

    async def one(self):
        query, params = self.get_raw_query()
        return await self._engine.fetchone(self._table, query, params)

    async def all(self):
        query, params = self.get_raw_query()
        return await self._engine.fetchall(self._table, query, params)

    def __repr__(self):
        query, params = self.get_raw_query()
        return f'<Query {query}, params={params}>'


class ResultQuery:
    def __init__(self, table, results):
        self._table = table
        self._results = results

    def __iter__(self):
        for elem in self._results:
            yield self._table(**elem)

    def __getitem__(self, idx):
        return self._table(**self._results[idx])

    def __len__(self):
        return len(self._results)
