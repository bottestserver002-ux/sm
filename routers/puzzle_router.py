from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import PuzzleLevel, PuzzleProgress
import cloudinary
import cloudinary.uploader
import os

router = APIRouter()

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


def get_size_by_level(level: int):
    if level == 1:
        return 3, 4
    if level == 2:
        return 4, 4
    if level == 3:
        return 5, 4
    if level == 4:
        return 5, 5
    if level == 5:
        return 6, 5
    if 6 <= level <= 30:
        return 7, 5
    return 8, 5


@router.get("/puzzle/levels")
def get_levels(email: str = "", db: Session = Depends(get_db)):
    levels = db.query(PuzzleLevel).order_by(PuzzleLevel.level.asc()).all()

    completed = []

    if email:
        completed = [
            p.level for p in db.query(PuzzleProgress)
            .filter(PuzzleProgress.email == email)
            .all()
        ]

    max_unlocked = 1

    if completed:
        max_unlocked = max(completed) + 1

    return [
        {
            "id": item.id,
            "level": item.level,
            "image": item.image,
            "rows": item.rows,
            "cols": item.cols,
            "locked": item.level > max_unlocked,
            "completed": item.level in completed
        }
        for item in levels
    ]


@router.post("/puzzle/level")
def upload_level(
    level: int = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    rows, cols = get_size_by_level(level)

    result = cloudinary.uploader.upload(
        image.file,
        folder="puzzle",
        width=1200,
        crop="limit",
        quality="auto",
        fetch_format="auto"
    )

    image_url = result["secure_url"]

    old = db.query(PuzzleLevel).filter(
        PuzzleLevel.level == level
    ).first()

    if old:
        old.image = image_url
        old.rows = rows
        old.cols = cols
    else:
        db.add(
            PuzzleLevel(
                level=level,
                image=image_url,
                rows=rows,
                cols=cols
            )
        )

    db.commit()

    return {"message": "Upload level thành công"}


@router.post("/puzzle/complete")
def complete_level(data: dict, db: Session = Depends(get_db)):
    email = data.get("email")
    level = data.get("level")

    if not email:
        return {"message": "Người chưa đăng nhập không lưu tiến độ"}

    exists = db.query(PuzzleProgress).filter(
        PuzzleProgress.email == email,
        PuzzleProgress.level == level
    ).first()

    if not exists:
        db.add(
            PuzzleProgress(
                email=email,
                level=level
            )
        )
        db.commit()

    return {"message": "Đã lưu tiến độ"}