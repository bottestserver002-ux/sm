from fastapi import APIRouter
from ai_chat import ask_ai

router = APIRouter()


@router.post("/ask-ai")
def ask(data: dict):
    if "message" not in data:
        raise HTTPException(400, "Missing message")

    try:
        answer = ask_ai(data["message"])
        return {"reply": answer}
    except Exception as e:
        return {"reply": f"Lỗi AI: {str(e)}"}