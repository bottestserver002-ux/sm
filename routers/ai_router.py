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

    post_length = data.get(
        "post_length",
        "Tự động"
    )

    # ==========================
    # THÊM ĐOẠN NÀY Ở ĐÂY
    # ==========================
    length_rule = """
- Rất ngắn: 80–150 từ.
- Ngắn: 150–300 từ.
- Trung bình: 300–600 từ.
- Dài: 600–1000 từ.
- SEO: 1000–1500 từ.
"""

    if post_length == "Tự động":

        if platform == "TikTok":
            length_rule = """
Viết khoảng 80–120 từ.
Ưu tiên hook mạnh, ngắn gọn,
dễ đọc trên điện thoại.
"""

        elif platform == "Instagram":
            length_rule = """
Viết khoảng 150–250 từ.
Ưu tiên cảm xúc,
storytelling nhẹ,
dễ kết hợp carousel.
"""

        elif platform == "Facebook":
            length_rule = """
Viết khoảng 250–500 từ.
Ưu tiên tương tác,
bình luận và chia sẻ.
"""

        elif platform == "Website":
            length_rule = """
Viết khoảng 1000–1500 từ.
Chuẩn SEO,
có heading,
từ khóa tự nhiên.
"""
    # ==========================
    # HẾT ĐOẠN THÊM
    # ==========================

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

ĐỘ DÀI FACEBOOK POST:
{post_length}

QUY TẮC ĐỘ DÀI:
{length_rule}

BẮT BUỘC tuân thủ quy tắc độ dài ở trên.

Hãy dựa vào chủ đề số {selected_idea_number} trong danh sách trên và tạo:

## 1. Facebook Post hoàn chỉnh

Yêu cầu:

- Hook mở đầu thật cuốn.
- Nội dung tự nhiên.
- Xuống dòng đẹp.
- Có CTA cuối bài.
- Không viết kiểu AI.
- Phù hợp đăng Facebook.

## 2. Gợi ý hình ảnh cho bài viết

Gợi ý từ 1 đến 5 ảnh.

Mỗi ảnh phải có:

- Nội dung ảnh.
- Bối cảnh.
- Góc chụp.
- Tone màu.
- Text overlay nếu cần.

## 3. Hashtag đề xuất

Đề xuất hashtag phù hợp.
"""

    try:
        response = model.generate_content(prompt)
        return {"result": response.text}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
        )