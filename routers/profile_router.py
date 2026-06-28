from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import User
import cloudinary.uploader
from datetime import datetime

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/{user_id}")
def get_profile(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "avatar": user.avatar,
        "birthday": str(user.birthday) if user.birthday else "",
        "job": user.job or "",
        "gender": user.gender or "",
    }


@router.put("/{user_id}")
async def update_profile(
    user_id: int,
    birthday: str = Form(None),
    job: str = Form(None),
    gender: str = Form(None),
    avatar: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy người dùng")



    if birthday:
       user.birthday = datetime.strptime(
           birthday,
           "%Y-%m-%d"
            ).date()

    user.job = job
    user.gender = gender

    if avatar:
        result = cloudinary.uploader.upload(
            avatar.file,
            folder="personal_website/avatar"
        )
        user.avatar = result["secure_url"]

    db.commit()
    db.refresh(user)

    return {
        "message": "Cập nhật thông tin thành công",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "avatar": user.avatar,
            "birthday": str(user.birthday) if user.birthday else "",
            "job": user.job or "",
            "gender": user.gender or "",
        }
    }