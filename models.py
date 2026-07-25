from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, Date, ForeignKey
from sqlalchemy.sql import func
from database import Base
from sqlalchemy.orm import relationship

from datetime import datetime


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

# ==========================================================
# PLANNING MONTH
# ==========================================================

class PlanningMonth(Base):

    __tablename__ = "planning_month"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )

    title = Column(
        String(255),
        nullable=False
    )

    goal = Column(Text)

    note = Column(Text)

    start_date = Column(Date)

    end_date = Column(Date)

    status = Column(
        String(30),
        default="Doing"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    weeks = relationship(
        "PlanningWeek",
        back_populates="month",
        cascade="all, delete"
    )


# ==========================================================
# PLANNING WEEK
# ==========================================================

class PlanningWeek(Base):

    __tablename__ = "planning_week"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    month_id = Column(
        Integer,
        ForeignKey(
            "planning_month.id",
            ondelete="CASCADE"
        )
    )

    title = Column(
        String(150)
    )

    week_number = Column(
        Integer
    )

    goal = Column(Text)

    note = Column(Text)

    status = Column(
        String(30),
        default="Doing"
    )

    month = relationship(
        "PlanningMonth",
        back_populates="weeks"
    )

    days = relationship(
        "PlanningDay",
        back_populates="week",
        cascade="all, delete"
    )


# ==========================================================
# PLANNING DAY
# ==========================================================

class PlanningDay(Base):

    __tablename__ = "planning_day"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    week_id = Column(
        Integer,
        ForeignKey(
            "planning_week.id",
            ondelete="CASCADE"
        )
    )

    date = Column(Date)

    title = Column(
        String(255)
    )

    goal = Column(Text)

    note = Column(Text)

    status = Column(
        String(30),
        default="Doing"
    )

    week = relationship(
        "PlanningWeek",
        back_populates="days"
    )

    tasks = relationship(
        "PlanningTask",
        back_populates="day",
        cascade="all, delete"
    )


# ==========================================================
# PLANNING TASK
# ==========================================================

class PlanningTask(Base):

    __tablename__ = "planning_task"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    day_id = Column(
        Integer,
        ForeignKey(
            "planning_day.id",
            ondelete="CASCADE"
        )
    )

    title = Column(
        String(255),
        nullable=False
    )

    description = Column(Text)

    location = Column(
        String(255)
    )

    position = Column(
        String(255)
    )

    partner = Column(
        String(255)
    )

    start_time = Column(
        String(10)
    )

    end_time = Column(
        String(10)
    )

    deadline = Column(DateTime)

    priority = Column(
        String(20),
        default="Medium"
    )

    status = Column(
        String(20),
        default="Todo"
    )

    completed = Column(
        Boolean,
        default=False
    )

    note = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

    day = relationship(
        "PlanningDay",
        back_populates="tasks"
    )