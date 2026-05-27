from pydantic import BaseModel, EmailStr


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