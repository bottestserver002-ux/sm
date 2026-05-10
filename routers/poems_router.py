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