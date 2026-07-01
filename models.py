from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date
from sqlalchemy.sql import func
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    password = Column(String)

    is_admin = Column(Boolean, default=False)
    is_family = Column(Boolean, default=False)

    avatar = Column(Text, nullable=True)
    birthday = Column(Date, nullable=True)
    job = Column(String, nullable=True)
    gender = Column(String, nullable=True)

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

class OTPCode(Base):

    __tablename__ = "otp_codes"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    email = Column(
        String,
        nullable=False
    )

    otp = Column(
        String,
        nullable=False
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

class FoodItem(Base):
    __tablename__ = "food_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    image = Column(String, nullable=True)

class SiteVisit(Base):
    __tablename__ = "site_visits"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=True)
    user_agent = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class PuzzleLevel(Base):
    __tablename__ = "puzzle_levels"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(Integer, unique=True, index=True)
    image = Column(Text, nullable=False)
    rows = Column(Integer, nullable=False)
    cols = Column(Integer, nullable=False)


class PuzzleProgress(Base):
    __tablename__ = "puzzle_progress"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, index=True)
    level = Column(Integer, nullable=False)