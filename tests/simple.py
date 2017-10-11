from pprint import pprint

from sys import path
from os.path import join, dirname, abspath

path.insert(0, join(dirname(abspath(__file__)), '..'))


from sqlchemistry.session import Session
from sqlchemistry.types import Int, Boolean, Float, String
from sqlchemistry.sql.schema import Table, Column
from sqlchemistry.engine.backends.mysql import MySQLEngine


class User(Table):
    __tablename__ = 'users'

    id = Column(Int, primary_key=True, autoincrement=True)
    paco = Column(Float)
    jamones = Column(Float(5))
    salsicha = Column(Boolean)
    string = Column(String)


ss = Session(MySQLEngine(dsn="mysql+pymysql://a:b@host/db"))

print()
print(ss.create_table(User))
print('\n')


user = User()
user.jamones = 3
query = ss.query(User)\
          .where(User.paco == 6)\
          .where(User.jamones == user.jamones)

pprint(query.get_raw_query())
print()
