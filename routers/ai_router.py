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
        raise HTTPException(status_code=400, detail="Thiếu chủ đề")

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
Phân tích insight khách hàng mục tiêu thật sâu.

## 2. 20 ý tưởng chủ đề có khả năng viral
Liệt kê đúng 20 chủ đề.

Mỗi chủ đề cần có:
- Tên chủ đề.
- Vì sao chủ đề này dễ viral.
- Insight khách hàng liên quan.
- Điểm Viral: x/10.
- Điểm Chuyển đổi: x/10.

## 3. 3 hook mở đầu chung
Viết 3 hook có thể dùng cho nhiều bài.

## 4. Hashtag đề xuất
Đề xuất 10 hashtag liên quan.

Yêu cầu:
- Viết hoàn toàn bằng tiếng Việt tự nhiên.
- Không viết kiểu máy móc.
- Ưu tiên insight khách hàng, độ viral và khả năng chuyển đổi.
- Không viết 5 caption viral trong bước này.
"""

    try:
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
        )
    
@router.post("/generate-post")
def generate_post(data: dict):
    main_subject = data.get("main_subject", "")
    selected_idea_number = data.get("selected_idea_number", "")
    ideas_text = data.get("ideas_text", "")
    tone = data.get("tone", "Thân thiện")
    platform = data.get("platform", "Facebook")
    goal = data.get("goal", "Tăng tương tác")

    if not main_subject or not selected_idea_number:
        raise HTTPException(
            status_code=400,
            detail="Thiếu chủ đề hoặc số chủ đề đã chọn"
        )

    prompt = f"""
Bạn là chuyên gia Facebook Marketing Việt Nam.

CHỦ ĐỀ GỐC:
{main_subject}

NGƯỜI DÙNG CHỌN CHỦ ĐỀ SỐ:
{selected_idea_number}

DANH SÁCH 20 CHỦ ĐỀ ĐÃ TẠO:
{ideas_text}

NỀN TẢNG:
{platform}

MỤC TIÊU:
{goal}

VĂN PHONG:
{tone}

Hãy dựa vào chủ đề số {selected_idea_number} trong danh sách trên và tạo:

## 1. Facebook Post hoàn chỉnh
Yêu cầu:
- Có hook mở đầu thật cuốn.
- Nội dung tự nhiên, cảm xúc, dễ đọc.
- Có ngắt dòng đẹp.
- Có CTA cuối bài.
- Không viết kiểu AI.
- Phù hợp đăng Facebook.

## 2. Gợi ý hình ảnh cho bài viết
Gợi ý 1 đến 5 ảnh tùy nội dung.

Với mỗi ảnh ghi rõ:
- Nội dung ảnh.
- Bối cảnh.
- Góc chụp.
- Màu sắc/tone ảnh.
- Text overlay nếu cần.

## 3. Hashtag đề xuất
Đề xuất hashtag phù hợp với bài viết.
"""

    try:
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
        )