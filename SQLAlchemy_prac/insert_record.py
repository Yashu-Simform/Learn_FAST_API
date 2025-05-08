from dbmodels import User, Comment

from sqlalchemy.orm import Session
from db_connections import DBConnection

mydb = DBConnection()
mydb.create_engine()

session = Session(bind=mydb.engine)

captain_rogers = User(
    username="@captainrogers",
    email="captain.rogers@gmail.com",
    comments=[
        Comment(text="Avengers..! Assemble ho ne ka waqt aa gaya he."),
        Comment(text="Suit pehenlo Tony..!")
    ]
)

jack_sparrow = User(
    username="@jacksparrow",
    email="jack.sparrow@gmail.com",
    comments=[
        Comment(text="Where is the bloody rum!"),
        Comment(text="Ye mera ship he!")
    ]
)


session.add_all([captain_rogers, jack_sparrow])

session.commit()
print("Transaction has ended!")