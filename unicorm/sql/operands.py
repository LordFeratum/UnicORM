class Operation:
    _identifier = 0

    def __new__(cls, *args, **kwargs):
        Operation._identifier += 1
        return super(Operation, cls).__new__(cls)

    def __init__(self, table, column, value, right_column):
        self._id = Operation._identifier
        self._table = table
        self._column = column
        self._value = value
        self._right_column = right_column

    def get_parameter(self):
        return {self._get_identifier(): self._value}

    def _get_identifier(self):
        return '{tablename}_{column}_{identifier}'\
               .format(tablename=self._table.tablename(),
                       column=self._column.name,
                       identifier=self._id)

    def __and__(self, obj):
        return And(self, obj)

    def __or__(self, obj):
        return Or(self, obj)


class FilterOperation:
    def __init__(self, operation_a, operation_b):
        self._operation_a = operation_a
        self._operation_b = operation_b

    def _get_parameters(self):
        operations = {}
        for op in [self._operation_a, self._operation_b]:
            if isinstance(op, Operation):
                operations.update(op.get_parameter())

            elif isinstance(op, FilterOperation):
                operations.update(op._get_parameters())

            else:
                raise TypeError("Invalid type of operation.")

        return operations

    def get_parameter(self):
        return self._get_parameters()

    def get_operation_a(self, engine):
        return self._operation_a.get_operation(engine)

    def get_operation_b(self, engine):
        return self._operation_b.get_operation(engine)

    def get_unproccesed_operation_a(self, engine):
        return self._operation_a.get_unproccesed_operation(engine)

    def get_unproccesed_operation_b(self, engine):
        return self._operation_b.get_unproccesed_operation(engine)


class Equals(Operation):
    def get_operation(self, engine):
        params = {
            'tablename': self._table.tablename(),
            'column': self._column.name,
            'operand': engine.EQUALS,
            'id': engine.get_dbapi_identifier(self._get_identifier())
        }
        return '{tablename}.`{column}` {operand} {id}'.format(**params)

    def get_unproccesed_operation(self, engine):
        tablename = self._table.tablename()
        column = self._column.name
        operand = engine.EQUALS
        ntablename = self._right_column.tablename
        ncolumn = self._right_column.name
        return f'{tablename}.`{column}` {operand} {ntablename}.`{ncolumn}`'


class Is(Operation):
    def get_operation(self, engine):
        tablename = self._table.tablename()
        column = self._column.name
        operand = engine.IS
        _id = engine.get_dbapi_identifier(self._get_identifier())
        return f'{tablename}.`{column}` {operand} {_id}'

    def get_unproccesed_operation(self, engine):
        tablename = self._table.tablename()
        column = self._column.name
        operand = engine.IS
        ntablename = self._right_column.tablename
        ncolumn = self._right_column.name
        return f'{tablename}.`{column}` {operand} {ntablename}.`{ncolumn}`'


class And(FilterOperation):
    def get_operation(self, engine):
        op_a = self.get_operation_a(engine)
        op_b = self.get_operation_b(engine)
        operand = engine.AND
        return f'({op_a} {operand} {op_b})'

    def get_unproccesed_operation(self, engine):
        op_a = self.get_unproccesed_operation_a(engine)
        op_b = self.get_unproccesed_operation_b(engine)
        operand = engine.AND
        return f'{op_a} {operand} {op_b}'


class Or(FilterOperation):
    def get_operation(self, engine):
        op_a = self.get_operation_a(engine)
        op_b = self.get_operation_b(engine)
        operand = engine.OR
        return f'({op_a} {operand} {op_b})'

    def get_unproccesed_operation(self, engine):
        op_a = self.get_unproccesed_operation_a(engine)
        op_b = self.get_unproccesed_operation_b(engine)
        operand = engine.OR
        return f'{op_a} {operand} {op_b}'
