class AbstractType:
    def __init__(self, *args, **kwargs):
        self._value = None
        self._args = args
        self._kwargs = kwargs

    def _cast(self, value):
        return value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = self._cast(value)


class Int(AbstractType):
    def sql_type(self):
        return 'INTEGER'


class Float(AbstractType):
    def sql_type(self):
        max_len = self._kwargs.get('max_length')
        if max_len is None:
            return 'FLOAT'

        return 'FLOAT({})'.format(max_len)


class String(AbstractType):
    def sql_type(self):
        max_len = self._kwargs.get('max_length', 50)
        return 'VARCHAR({})'.format(max_len)


class Boolean(AbstractType):
    def _cast(self, value):
        return bool(value)

    def sql_type(self):
        return 'BOOLEAN'
