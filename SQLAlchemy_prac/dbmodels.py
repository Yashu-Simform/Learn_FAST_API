from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Text
from datetime import datetime
from typing import List

class Base(DeclarativeBase):
    # created_at: Mapped[datetime] = mapped_column(default=datetime.now())
    # updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    username: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    comments: Mapped[List["Comment"]] = relationship(back_populates="user") #relationship One-Many with user field of Comment

    def __repr__(self):
        return f"<User username={self.username}>"

class Comment(Base):
    __tablename__ = 'comments'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    text: Mapped[str] = mapped_column(Text)
    user: Mapped[User] = relationship(back_populates="comments")    #relationship Many-one with commments field of Comment

    def __repr__(self):
        return f"<Comment text={self.text} by user={self.user.username}>"
