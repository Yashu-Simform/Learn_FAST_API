from dbmodels import Base, User, Comment

from db_connections import DBConnection

mydb = DBConnection()
mydb.create_engine()

Base.metadata.create_all(bind=mydb.engine)