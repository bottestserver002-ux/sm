from pydantic import BaseModel, EmailStr
from datetime import date, datetime
from typing import Optional


class RegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class LoginSchema(BaseModel):
    email: EmailStr
    password: str

# =========================
# MINI GAME
# =========================

class QuestionCreate(BaseModel):
    image: str
    answer: str


class QuestionOut(BaseModel):
    id: int
    image: str
    answer: str
    letters: list[str]

    class Config:
        from_attributes = True

# ==========================================================
# MONTH
# ==========================================================

class MonthCreate(BaseModel):

    user_id: int

    title: str

    goal: Optional[str] = None

    note: Optional[str] = None

    start_date: date

    end_date: date


class MonthUpdate(BaseModel):

    title: str

    goal: Optional[str] = None

    note: Optional[str] = None

    start_date: date

    end_date: date

    status: str


# ==========================================================
# WEEK
# ==========================================================

class WeekCreate(BaseModel):

    month_id: int

    title: str

    week_number: int

    goal: Optional[str] = None

    note: Optional[str] = None


class WeekUpdate(BaseModel):

    title: str

    week_number: int

    goal: Optional[str] = None

    note: Optional[str] = None

    status: str


# ==========================================================
# DAY
# ==========================================================

class DayCreate(BaseModel):

    week_id: int

    date: date

    title: str

    goal: Optional[str] = None

    note: Optional[str] = None


class DayUpdate(BaseModel):

    date: date

    title: str

    goal: Optional[str] = None

    note: Optional[str] = None

    status: str


# ==========================================================
# TASK
# ==========================================================

class TaskCreate(BaseModel):

    day_id: int

    title: str

    description: Optional[str] = None

    location: Optional[str] = None

    position: Optional[str] = None

    partner: Optional[str] = None

    start_time: str

    end_time: str

    deadline: Optional[datetime] = None

    priority: str = "Medium"

    note: Optional[str] = None


class TaskUpdate(BaseModel):

    title: str

    description: Optional[str] = None

    location: Optional[str] = None

    position: Optional[str] = None

    partner: Optional[str] = None

    start_time: str

    end_time: str

    deadline: Optional[datetime] = None

    priority: str

    status: str

    completed: bool

    note: Optional[str] = None


# ==========================================================
# RESPONSE
# ==========================================================

class ProgressResponse(BaseModel):

    total: int

    completed: int

    doing: int

    expired: int

    progress: float


class DashboardResponse(BaseModel):

    today_tasks: int

    completed: int

    doing: int

    expired: int

    progress: float


class SearchTask(BaseModel):

    keyword: str