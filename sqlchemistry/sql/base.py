class BaseQuery:
    def __init__(self, table, columns=None):
        if columns is not None and isinstance(columns, list):
            raise TypeError("columns must be a list")

        self._from = table.tablename()
        self._columns = columns or table.columns()

    def where(self, condition):
        pass
