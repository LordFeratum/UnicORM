class BaseQuery:
    def __init__(self, table, columns=None):
        if columns is not None and isinstance(columns, list):
            raise TypeError("columns must be a list")

        self._from = getattr(table, '__tablename__', table.__name__.lower())
        self._columns = columns or [attr for attr in table.__dict__
                                    if not attr.startswith('__')]

    def where(self, condition):
        pass
