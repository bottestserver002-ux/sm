from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Poem

router = APIRouter()


# GET ALL + FILTER CATEGORY
@router.get("/poems")
def get_poems(category: str = None, db: Session = Depends(get_db)):

    query = db.query(Poem)

    if category and category != "all":
        query = query.filter(Poem.category == category)

    return query.all()


# ADD POEM (ADMIN ONLY - tạm chưa check token nâng cao)
@router.post("/poems")
def add_poem(data: dict, db: Session = Depends(get_db)):

    new_poem = Poem(
        title=data["title"],
        content=data["content"],
        category=data["category"]
    )

    db.add(new_poem)
    db.commit()

    return {"message": "Thêm bài thơ thành công"}

# UPDATE POEM
@router.put("/poems/{id}")
def update_poem(id: int, data: dict, db: Session = Depends(get_db)):

    poem = db.query(Poem).filter(Poem.id == id).first()

    if not poem:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài thơ")

    poem.title = data["title"]
    poem.content = data["content"]
    poem.category = data["category"]

    db.commit()

    return {"message": "Cập nhật thành công"}


# DELETE POEM
@router.delete("/poems/{id}")
def delete_poem(id: int, db: Session = Depends(get_db)):

    poem = db.query(Poem).filter(Poem.id == id).first()

    if not poem:
        raise HTTPException(status_code=404, detail="Không tìm thấy bài thơ")

    db.delete(poem)

    db.commit()

    return {"message": "Xóa thành công"}