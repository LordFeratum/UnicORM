

class Operation:
    def __init__(self, table, column, value):
        self._table = table
        self._column = column
        self._value = value


class Equals(Operation):
    def get_operation(self, engine):
        return ''
