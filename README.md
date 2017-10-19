# SQLChemistry
A simple python 3.6+ asynchronous data mapper ORM.

This ORM intends to provide the simpliest API to interact with your database.

## Examples

### Model definition
```
from sqlchemistry.types import Int, String
from sqlchemistry.sql.schema import Table, Column

class User(Table):
    __tablename__ = 'users'

    id = Column(Int, primary_key=True, autoincrement=True)
    username = Column(String)
    email = Column(String)
```

### Create database
```
from sqlchemistry.session import Session
from sqlchemistry.engine.backends.mysql import MySQLEngine

session = Session(MySQLEngine(dsn=dsn, loop=loop))
await session.connect()
await session.create_table_if_not_exists(User)
```

### Insert new element
```
user = User(username="Patri", email="pgonzest@email.com")
await session.insert(user)

# if autocommit is False then
# await session.commit()
```

### Querying
```
from operator import and_

query = session.query(User)\
               .where(and_(User.username == 'Patri',
                           User.email == 'pgonzest@email.com'))

patri = await query.one()
patris = await query.all()
```

## TODO
- Implement all types (Actually only support: Int, String, Float and Boolean)
- Implement pool of connections
- Implement relationships
- So much work to do...
- Support PostgreSQL engine
