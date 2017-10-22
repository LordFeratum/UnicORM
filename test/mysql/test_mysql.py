import pytest

from os import environ

from unicorm.engine.backends.mysql import MySQLEngine
from unicorm.sql.schema import Table, Column
from unicorm.types import Int, Boolean, Float, String, ForeignKey
from unicorm.session import Session


class User(Table):
    __tablename__ = 'users'
    id = Column(Int, primary_key=True, autoincrement=True)
    name = Column(String)


@pytest.mark.asyncio
async def test_simple_create_database(event_loop):
    dsn = environ.get("DB_DSN")
    session = Session(MySQLEngine(dsn=dsn, loop=event_loop))
    await session.connect()
    await session.create_table(User)
