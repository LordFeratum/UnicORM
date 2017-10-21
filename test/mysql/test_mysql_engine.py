import pytest

from sqlchemistry.engine.backends.mysql import MySQLEngine


@pytest.yield_fixture
def engine(event_loop):
    dsn = "mysql+pymysql://user:user@mysql/database"
    engine = MySQLEngine(dsn=dsn, loop=event_loop)
    yield engine


def test_dbapi_identifier(engine):
    identifier = engine.get_dbapi_identifier("id")
    assert identifier == '%(id)s'
