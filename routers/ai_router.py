from fastapi import APIRouter, HTTPException
from ai_chat import model, ask_ai
import os
import google.generativeai as genai

router = APIRouter()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(
    api_key=GEMINI_API_KEY
)

model = genai.GenerativeModel("gemini-2.5-flash")


@router.post("/ask-ai")
def ask(data: dict):
    if "message" not in data:
        raise HTTPException(400, "Missing message")

    try:
        answer = ask_ai(data["message"])
        return {"reply": answer}
    except Exception as e:
        return {"reply": f"Lỗi AI: {str(e)}"}


@router.post("/auto-caption")
def auto_caption(data: dict):
    topic = data.get("topic", "")
    platform = data.get("platform", "Facebook")
    goal = data.get("goal", "Tăng tương tác")
    tone = data.get("tone", "Thân thiện")
    length = data.get("length", "Trung bình")

    google_suggest = data.get("google_suggest", [])
    google_trends = data.get("google_trends", [])

    if not topic:
        raise HTTPException(
            status_code=400,
            detail="Thiếu chủ đề"
        )

    prompt = f"""
Bạn là chuyên gia SEO và Social Media Marketing Việt Nam.

CHỦ ĐỀ:
{topic}

NỀN TẢNG:
{platform}

MỤC TIÊU:
{goal}

VĂN PHONG:
{tone}

ĐỘ DÀI:
{length}

GOOGLE SUGGEST:
{google_suggest}

GOOGLE TRENDS:
{google_trends}

Hãy tạo nội dung theo cấu trúc sau:

## 1. Insight khách hàng
Phân tích insight khách hàng mục tiêu.

## 2. 10 ý tưởng chủ đề
Liệt kê 10 ý tưởng chủ đề hấp dẫn.

## 3. 5 caption viral
Viết 5 caption phù hợp với nền tảng {platform}.

## 4. Bài viết chuẩn SEO
Viết 1 bài chuẩn SEO hoàn chỉnh, có tiêu đề, sapo, các heading H2/H3.

## 5. 3 hook mở đầu
Viết 3 hook mở đầu thu hút.

## 6. Hashtag đề xuất
Đề xuất 10 hashtag liên quan.

## 7. 3 ý tưởng Reel
Đề xuất 3 ý tưởng video/Reel ngắn.

## 8. Lịch đăng bài tối ưu
Đề xuất lịch đăng bài trong 7 ngày.

Yêu cầu:
- Viết hoàn toàn bằng tiếng Việt tự nhiên.
- Không viết kiểu máy móc.
- Ưu tiên khả năng viral, tương tác và SEO Google.
- Nội dung phải thực tế, dễ dùng ngay.
"""

    try:
        response = model.generate_content(prompt)

        return {
            "result": response.text
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
        )