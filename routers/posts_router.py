from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Post

router = APIRouter()


@router.get("/posts")
def get_posts(db: Session = Depends(get_db)):

    return db.query(Post).order_by(Post.id.desc()).all()


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

# UPDATE POST
@router.put("/posts/{id}")
def update_post(id: int, data: dict, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        return {"message": "Không tìm thấy bài viết"}

    post.title = data["title"]
    post.image = data["image"]
    post.content = data["content"]

    db.commit()

    return {"message": "Cập nhật thành công"}


# DELETE POST
@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db)):

    post = db.query(Post).filter(Post.id == id).first()

    if not post:
        return {"message": "Không tìm thấy bài viết"}

    db.delete(post)

    db.commit()

    return {"message": "Xóa thành công"}