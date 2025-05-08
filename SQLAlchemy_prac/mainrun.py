from sqlalchemy.orm import Session
from db_connections import DBConnection
from dbmodels import User
from sql_statement import statement2

mydb = DBConnection()
mydb.create_engine()
session = mydb.create_session()

result = session.scalars(statement2)
r1 = session.query(User).filter_by(username="@captainrogers").first()
print(r1)

# for e in r2:
#     print(e)