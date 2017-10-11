class BaseQuery:
    def __init__(self, engine, table, columns=None):
        if not isinstance(columns, list):
            raise TypeError("columns must be a list")

        self._engine = engine
        self._from = table.tablename()
        self._columns = columns or table.columns()
        self._conditions = []
        self._parameters = {}

    def where(self, condition):
        self._parameters.update(condition.get_parameter())
        operation = condition.get_operation(self._engine)
        self._conditions.append(operation)
        return self
