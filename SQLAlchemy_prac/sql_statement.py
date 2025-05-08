from sqlalchemy import select
from dbmodels import User, Comment

# statement = select(User)
statement2 = select(User).where(User.username.in_(['@captainrogers', '@jacksparrow']))