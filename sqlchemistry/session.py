class Session:
    def __init__(self, engine):
        self._engine = engine

    def query(self, table, columns=None):
        return self._engine.get_query(table, columns=columns)
