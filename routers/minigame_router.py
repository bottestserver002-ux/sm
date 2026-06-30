from fastapi import (
    APIRouter,
    Depends,
    UploadFile,
    File,
    Form
)

from sqlalchemy.orm import Session

from database import get_db
from models import Question

import random
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


# =========================
# GET QUESTIONS
# =========================

@router.get("/minigame")
def get_questions(
    db: Session = Depends(get_db)
):

    questions = db.query(Question).all()

    result = []

    for q in questions:

        answer = q.answer.upper().replace(" ", "")

        extra = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

        letters = list(answer)

        while len(letters) < 20:

            letters.append(
                random.choice(extra)
            )

        random.shuffle(letters)

        result.append({
            "id": q.id,
            "image": q.image,
            "answer": answer,
            "letters": letters
        })

    return result


# =========================
# ADD QUESTION
# =========================

@router.post("/minigame")
def add_question(
    answer: str = Form(...),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    try:

        # Upload Cloudinary
        result = cloudinary.uploader.upload(
        image.file,
        folder="minigame",
        width=800,
        crop="limit",
        quality="auto",
        fetch_format="auto"
        )

        image_url = result["secure_url"]

        new_question = Question(
            image=image_url,
            answer=answer
        )

        db.add(new_question)
        db.commit()

        return {
            "message": "Thêm thành công"
        }

    except Exception as e:

        return {
            "message": f"Lỗi upload: {str(e)}"
        }

# =========================
# DELETE QUESTION
# =========================

@router.delete("/minigame/{id}")
def delete_question(
    id: int,
    db: Session = Depends(get_db)
):

    q = db.query(Question).filter(
        Question.id == id
    ).first()

    if not q:

        return {
            "message": "Không tìm thấy câu hỏi"
        }

    db.delete(q)

    db.commit()

    return {
        "message": "Xóa thành công"
    }