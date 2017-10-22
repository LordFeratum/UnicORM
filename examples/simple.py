from time import sleep

from asyncio import get_event_loop

from unicorm.session import Session
from unicorm.types import Int, Boolean, Float, String, ForeignKey
from unicorm.sql.schema import Table, Column
from unicorm.engine.backends.mysql import MySQLEngine


loop = get_event_loop()


class User(Table):
    __tablename__ = 'users'

    id = Column(Int, primary_key=True, autoincrement=True)
    paco = Column(Float)
    jamones = Column(Float(5))
    salsicha = Column(Boolean)
    string = Column(String)


class Resume(Table):
    __tablename__ = 'resumes'

    id = Column(Int, primary_key=True, autoincrement=True)
    title = Column(String)

    user_id = Column(Int, ForeignKey(User.id))


async def main():
    dsn = "mysql+pymysql://user:user@mysql/sqlchemistry"
    ss = Session(MySQLEngine(dsn=dsn, loop=loop, use_pool=True,
                             autocommit=True, echo=True))
    await ss.connect()
    await ss.create_table_if_not_exists(User)
    await ss.create_table_if_not_exists(Resume)

    user = User(paco=1.0, jamones=2.3, salsicha=True, string="Miquel")
    await ss.insert(user)
    resume = Resume(title="Resume of Miquel!", user_id=user.id)
    await ss.insert(resume)

    query = ss.query(User)\
              .left_join(Resume, on=User.id == Resume.user_id)\
              .where(Resume.title == 'Resume of Miquel!')

    miquel = await query.one()
    print(miquel)

    await ss.delete(resume)
    print(resume)


if __name__ == '__main__':
    print("Waiting MySQL")
    sleep(10)
    loop.run_until_complete(main())
