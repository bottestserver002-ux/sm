from fastapi import APIRouter, HTTPException
from ai_chat import model, ask_ai
import os
import google.generativeai as genai

router = APIRouter()

API_KEYS = [
    os.getenv("GEMINI_API_KEY_1"),
    os.getenv("GEMINI_API_KEY_2"),
    os.getenv("GEMINI_API_KEY_3"),
]

API_KEYS = [x for x in API_KEYS if x]


def generate_content(prompt):

    last_error = None

    for key in API_KEYS:

        try:

            genai.configure(api_key=key)

            model = genai.GenerativeModel(
                "gemini-2.5-flash"
            )

            response = model.generate_content(
                prompt
            )

            return response.text

        except Exception as e:

            last_error = e

            print(f"KEY ERROR: {key[:10]}...")

            continue

    raise Exception(
        f"Tất cả API đều lỗi: {last_error}"
    )


def ask_ai(message):
    return generate_content(message)


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
        result = generate_content(prompt)
        return {"result": result}
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
- Rất ngắn: 80-150 từ.
- Ngắn: 150-300 từ.
- Trung bình: 300-600 từ.
- Dài: 600-1000 từ.
- SEO: 1000-1500 từ.
"""

    if post_length == "Tự động":

        if platform == "TikTok":
            length_rule = """
Viết khoảng 80-120 từ.
Ưu tiên hook mạnh, ngắn gọn,
dễ đọc trên điện thoại.
"""

        elif platform == "Instagram":
            length_rule = """
Viết khoảng 150-250 từ.
Ưu tiên cảm xúc,
storytelling nhẹ,
dễ kết hợp carousel.
"""

        elif platform == "Facebook":
            length_rule = """
Viết khoảng 250-500 từ.
Ưu tiên tương tác,
bình luận và chia sẻ.
"""

        elif platform == "Website":
            length_rule = """
Viết khoảng 1000-1500 từ.
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
        result = generate_content(prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
        )

@router.post("/generate-blog")
def generate_blog(data: dict):

    main_subject = data.get(
        "main_subject", ""
    )

    selected_idea_number = data.get(
        "selected_idea_number", ""
    )

    ideas_text = data.get(
        "ideas_text", ""
    )

    tone = data.get(
        "tone",
        "Thân thiện"
    )

    length = data.get(
        "length",
        "Dài"
    )

    prompt = f"""
Bạn là chuyên gia SEO Content Việt Nam năm 2026.

CHỦ ĐỀ GỐC:
{main_subject}

CHỦ ĐỀ ĐƯỢC CHỌN:
{selected_idea_number}

DANH SÁCH 20 Ý TƯỞNG:
{ideas_text}

VĂN PHONG:
{tone}

ĐỘ DÀI:
{length}

Hãy tạo:

# 1. Tiêu đề SEO

Đưa ra 3 tiêu đề khác nhau.

Mỗi tiêu đề:
- Tối đa 60 ký tự.
- Thu hút click.
- Chuẩn SEO.

# 2. Meta Description

- 140-160 ký tự.
- Chứa từ khóa chính.

# 3. URL Slug

Ví dụ:

khoa-dao-tao-hlv-yoga-200h-can-tho

# 4. Từ khóa chính

# 5. 10 từ khóa phụ

# 6. Search Intent

Phân loại:

- Informational
- Commercial
- Transactional
- Navigational

Giải thích lý do.

# 7. Internal Link gợi ý

Đề xuất 5 bài viết liên quan.

Ví dụ:

- Lợi ích của Yoga đối với dân văn phòng
- Hành trình trở thành HLV Yoga chuyên nghiệp
- ...

# 8. External Link gợi ý

Đề xuất nguồn uy tín:

- Yoga Alliance
- Bộ Y tế
- WHO
- ...

# 9. Outline bài viết

H1:

H2:

H3:

Phải logic và chuẩn SEO.

# 10. Bài viết hoàn chỉnh

Yêu cầu:

- 1200-1800 từ.
- Có mở bài.
- Có H2.
- Có H3.
- Có bullet points.
- Có CTA cuối bài.
- Không viết kiểu AI.
- Văn phong tự nhiên.
- Tối ưu SEO 2026.

# 11. FAQ

Viết 5 câu hỏi thường gặp.

Ví dụ:

Q: Học HLV Yoga 200H mất bao lâu?

A: ...

# 12. FAQ Schema JSON-LD

Sinh JSON-LD chuẩn.

# 13. Gợi ý hình ảnh

Cho 5 ảnh.

Mỗi ảnh:

- Nội dung ảnh.
- Góc chụp.
- Tone màu.
- Text overlay.

# 14. CTA cuối bài

Viết 3 CTA khác nhau:

- Mềm mại
- Bán hàng
- Xây thương hiệu

Toàn bộ phải viết bằng tiếng Việt tự nhiên.

Không dùng quá nhiều dấu # hoặc ***.

Markdown sạch, đẹp, dễ đọc.
"""

    try:
        result = generate_content(prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
    )

@router.post("/generate-tiktok")
def generate_tiktok(data: dict):

    main_subject = data.get(
        "main_subject", ""
    )

    selected_idea_number = data.get(
        "selected_idea_number", ""
    )

    ideas_text = data.get(
        "ideas_text", ""
    )

    tone = data.get(
        "tone",
        "Thân thiện"
    )

    prompt = f"""
Bạn là chuyên gia TikTok Marketing Việt Nam.

CHỦ ĐỀ GỐC:
{main_subject}

CHỦ ĐỀ ĐƯỢC CHỌN:
{selected_idea_number}

DANH SÁCH Ý TƯỞNG:
{ideas_text}

VĂN PHONG:
{tone}

Hãy tạo:

# 1. Hook mở đầu (3 giây đầu)

# 2. Kịch bản video 15-30 giây

Cảnh 1:
...

Cảnh 2:
...

# 3. Caption TikTok

80-120 từ.

# 4. Text overlay từng cảnh

# 5. Hiệu ứng chuyển cảnh

# 6. Nhạc nền phù hợp

# 7. Hashtag

# 8. CTA cuối video

Viết thật tự nhiên,
ưu tiên viral,
không viết kiểu AI.
"""

    try:
        result = generate_content(prompt)
        return {"result": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi Gemini: {str(e)}"
        )
