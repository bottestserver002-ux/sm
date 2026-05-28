from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Question

import random

router = APIRouter()


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
    data: dict,
    db: Session = Depends(get_db)
):

    image = data["image"]

    # AUTO CONVERT GOOGLE DRIVE
    if "drive.google.com/file/d/" in image:

        file_id = image.split("/d/")[1].split("/")[0]

        image = f"https://drive.google.com/uc?export=view&id={file_id}"

    new_question = Question(
        image=image,
        answer=data["answer"]
    )

    db.add(new_question)

    db.commit()

    return {
        "message": "Thêm câu hỏi thành công"
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