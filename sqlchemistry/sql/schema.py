from sqlchemistry.types import AbstractType


class Column:
    def __init__(self, column_type, **kwargs):
        if isinstance(column_type, AbstractType):
            self._column_type = column_type
        else:
            self._column_type = column_type()

        self._name = kwargs.get('name')
        self._kwargs = kwargs

    def is_primary_key(self):
        return self._kwargs.get('primary_key', False)

    def is_autoincrement(self):
        return self._kwargs.get('autoincrement', False)

    @property
    def sql_type(self):
        return self._column_type.sql_type()

    def set_name(self, column_name):
        if self._name is None:
            self._name = column_name

    @property
    def name(self):
        return self._name

    def __str__(self):
        ctype = self._column_type.sql_type()
        return '<{}: {}>'.format(self._name, ctype)

    def __repr__(self):
        return self.__str__()


class Table:
    @classmethod
    def tablename(cls):
        return getattr(cls, '__tablename__', cls.__name__.lower())

    @classmethod
    def columns(cls):
        def process_column(column, column_name):
            column.set_name(column_name)
            return column

        return [process_column(ctype, attr)
                for attr, ctype in cls.__dict__.items()
                if isinstance(ctype, Column)]

    @classmethod
    def primary_key(cls):
        for attr, ctype in cls.__dict__.items():
            if isinstance(ctype, Column) and ctype.is_primary_key():
                ctype.set_name(attr)
                return ctype

        return None
