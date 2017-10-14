class Operation:
    _identifier = 0

    def __new__(cls, *args, **kwargs):
        Operation._identifier += 1
        return super(Operation, cls).__new__(cls)

    def __init__(self, table, column, value):
        self._id = Operation._identifier
        self._table = table
        self._column = column
        self._value = value

    def get_parameter(self):
        return {self._get_identifier(): self._value}

    def _get_identifier(self):
        return '{tablename}_{column}_{identifier}'\
               .format(tablename=self._table.tablename(),
                       column=self._column.name,
                       identifier=self._id)


class Equals(Operation):
    def get_operation(self, engine):
        params = {
            'tablename': self._table.tablename(),
            'column': self._column.name,
            'operand': engine.EQUALS,
            'id': engine.get_dbapi_identifier(self._get_identifier())
        }
        return '{tablename}.`{column}` {operand} {id}'.format(**params)


class And(Operation):
    def get_operation(self, engine):
        pass


class Or(Operation):
    def get_operation(self, engine):
        pass
