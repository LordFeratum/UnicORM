from sqlchemistry.session import Session
from sqlchemistry.engine.backends.mysql import MySQLEngine


class User:
    __tablename__ = 'users'

    id = 1
    paco = ''
    jamones = ''


session = Session(MySQLEngine(dsn="mysql+pymysql://a:b@db/name"))

q = session.query(User)

print(q.get_raw_query())
