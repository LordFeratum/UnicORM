from unicorm.types import AbstractType, ForeignKey
from unicorm.sql.operands import Equals, Is


class Column:
    def __init__(self, column_type, *args, **kwargs):
        if isinstance(column_type, AbstractType):
            self._column_type = column_type
        else:
            self._column_type = column_type()

        self._table = None
        self._name = kwargs.get('name')
        self._args = args
        self._kwargs = kwargs

    def is_foreign_key(self):
        return any(isinstance(arg, ForeignKey) for arg in self._args)

    def get_foreign_key(self):
        for arg in self._args:
            if isinstance(arg, ForeignKey):
                return arg.parent_column

        return None

    def is_primary_key(self):
        return self._kwargs.get('primary_key', False)

    def is_autoincrement(self):
        return self._kwargs.get('autoincrement', False)

    def is_nullable(self):
        if self.is_primary_key():
            return True

        return self._kwargs.get('nullable', False)

    @property
    def sql_type(self):
        return self._column_type.sql_type()

    def set_name(self, column_name):
        if self._name is None:
            self._name = column_name

    def set_value(self, value):
        self._column_type.value = value

    def set_table(self, table):
        self._table = table

    def get_value(self):
        return self._column_type.value

    def get_table(self):
        return self._table

    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._column_type.value

    @property
    def tablename(self):
        return self._table.tablename()

    def __repr__(self):
        return '<{}: {}>'.format(self.sql_type, self.get_value())

    def __eq__(self, obj):
        value = obj
        if isinstance(obj, Column):
            value = obj.get_value()

        return Equals(self._table, self, value, obj)

    def is_(self, obj):
        value = obj
        if isinstance(obj, Column):
            value = obj.get_value()

        return Is(self._table, self, value, obj)


class Table:
    def __new__(cls, **kwargs):
        cls._init_columns(kwargs)
        return super(Table, cls).__new__(cls)

    @classmethod
    def _init_columns(cls, values):
        for name, column in cls.__dict__.items():
            if isinstance(column, Column):
                column.set_table(cls)
                column.set_name(name)
                value = values.get(name)
                if isinstance(value, Column):
                    value = value.get_value()

                column.set_value(value)

    @classmethod
    def tablename(cls):
        return getattr(cls, '__tablename__', cls.__name__.lower())

    @classmethod
    def columns(cls):
        return [ctype for ctype in cls.__dict__.values()
                if isinstance(ctype, Column)]

    @classmethod
    def primary_keys(cls):
        return [ctype for ctype in cls.columns()
                if ctype.is_primary_key()]

    def __setattr__(self, column, value):
        Table._init_columns({column: value})
        for attr, ctype in self.__class__.__dict__.items():
            if isinstance(ctype, Column) and attr == column:
                ctype.set_value(value)

    def __repr__(self):
        c = ', '.join(f'{c.name}: {c.get_value()}' for c in self.columns())
        return f"<{self.__class__.__name__} {c}>"
