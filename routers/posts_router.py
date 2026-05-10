from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Post

router = APIRouter()


@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    return db.query(Post).all()


@router.post("/posts")
def add_post(data: dict, db: Session = Depends(get_db)):

    new_post = Post(
        title=data["title"],
        image=data["image"],
        content=data["content"]
    )

    db.add(new_post)

    db.commit()

    return {
        "message": "Đăng bài thành công"
    }