from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database import get_db
from models import FoodItem
import resend
import cloudinary
import cloudinary.uploader
import os

router = APIRouter()

ADMIN_EMAIL = "bottestserver002@gmail.com"

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)


@router.get("/foods")
def get_foods(db: Session = Depends(get_db)):
    foods = db.query(FoodItem).order_by(
        FoodItem.name.asc()
    ).all()

    return [
        {
            "id": f.id,
            "name": f.name,
            "category": f.category,
            "image": f.image
        }
        for f in foods
    ]


@router.post("/foods")
def add_food(
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    image_url = None

    if image:
        upload_result = cloudinary.uploader.upload(
            image.file,
            folder="booking_food"
        )

        image_url = upload_result["secure_url"]

    food = FoodItem(
        name=name,
        category=category,
        image=image_url
    )

    db.add(food)
    db.commit()
    db.refresh(food)

    return {
        "message": "Đã thêm món",
        "food": {
            "id": food.id,
            "name": food.name,
            "category": food.category,
            "image": food.image
        }
    }


@router.put("/foods/{food_id}")
def update_food(
    food_id: int,
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    food = db.query(FoodItem).filter(
        FoodItem.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy món"
        )

    food.name = name
    food.category = category

    if image:
        upload_result = cloudinary.uploader.upload(
            image.file,
            folder="booking_food"
        )

        food.image = upload_result["secure_url"]

    db.commit()

    return {
        "message": "Đã cập nhật món"
    }


@router.delete("/foods/{food_id}")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(FoodItem).filter(
        FoodItem.id == food_id
    ).first()

    if not food:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy món"
        )

    db.delete(food)
    db.commit()

    return {
        "message": "Đã xóa món"
    }


@router.post("/foods/order")
def order_food(data: dict):
    items = data["items"]
    meal_time = data["meal_time"]
    username = data.get("username", "Không rõ")
    email = data.get("email", "Không rõ")

    item_list = "".join([
        f"<li>{item['name']} - {item['category']}</li>"
        for item in items
    ])

    html = f"""
    <h2>Đơn Booking Food mới</h2>

    <p><b>Người đặt:</b> {username}</p>
    <p><b>Email:</b> {email}</p>
    <p><b>Buổi ăn:</b> {meal_time}</p>

    <h3>Danh sách món:</h3>
    <ul>
        {item_list}
    </ul>
    """

    try:
        resend.Emails.send({
            "from": "Booking Food <no-reply@manhtruong6723.id.vn>",
            "to": ADMIN_EMAIL,
            "subject": "Đơn Booking Food mới",
            "html": html
        })

        return {
            "message": "Bạn đã oder món thành công"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi gửi order: {str(e)}"
        )


@router.get("/test-cloudinary")
def test_cloudinary():
    result = cloudinary.uploader.upload(
        "https://res.cloudinary.com/demo/image/upload/sample.jpg",
        folder="booking_food"
    )

    return result["secure_url"]