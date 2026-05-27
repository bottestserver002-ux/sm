from sqlalchemy import Column, Integer, String, Text, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    is_admin = Column(Boolean, default=False)


class Poem(Base):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    category = Column(String)  # ⭐ thêm thể loại


class Post(Base):

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True)

    title = Column(String)

    image = Column(String)

    content = Column(Text)

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)

    image = Column(Text, nullable=False)

    answer = Column(String(100), nullable=False)