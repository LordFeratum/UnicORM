from sqlchemistry.engine.base import BaseEngine


def test_base_engine_dsn(event_loop):
    dsn = "mysql+pymysql://user:user@mysql/database"
    expected_user = "user"
    expected_pwd = "user"
    expected_host = "mysql"
    expected_db = "database"

    engine = BaseEngine(dsn=dsn, loop=event_loop)

    assert engine._user == expected_user
    assert engine._pwd == expected_pwd
    assert engine._host == expected_host
    assert engine._db == expected_db
    assert engine._loop == event_loop
