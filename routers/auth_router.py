from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()


@router.post("/register")
def register(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data["email"]).first()

    if user:
        raise HTTPException(400, "Email đã tồn tại")

    new_user = User(
        username=data["username"],
        email=data["email"],
        password=hash_password(data["password"]),
        is_admin=False
    )

    db.add(new_user)
    db.commit()

    return {"message": "Đăng ký thành công"}


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data["email"]).first()

    if not user:
        raise HTTPException(400, "Sai tài khoản")

    if not verify_password(data["password"], user.password):
        raise HTTPException(400, "Sai mật khẩu")

    token = create_access_token({
        "id": user.id,
        "email": user.email,
        "is_admin": user.is_admin
    })

    return {
         "token": token,
    "is_admin": user.is_admin,
    "username": user.username,
    "email": user.email
    }