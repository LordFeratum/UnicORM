from datetime import datetime


class AbstractType:
    def __init__(self, *args, **kwargs):
        self._value = None
        self._args = args
        self._kwargs = kwargs

    def sql_cast(self, value):
        return value

    def get_sql_value(self):
        return self._sql_cast(self._value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class ForeignKey:
    def __init__(self, column):
        self._column = column

    @property
    def parent_column(self):
        return self._column


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
    def sql_cast(self, value):
        return 'TRUE' if value else 'FALSE'

    def sql_type(self):
        return 'BOOLEAN'


class DateTime(AbstractType):
    def sql_cast(self, value):
        date_format = '%Y-%m-%d %H:%M:%S'
        return datetime.strptime(value, date_format)

    def sql_type(self):
        return 'DATETIME'


class Date(AbstractType):
    def sql_cast(self, value):
        date_format = '%Y-%m-%d'
        return datetime.strptime(value, date_format).date()

    def sql_type(self):
        return 'DATE'
