from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
import shutil
from sqlalchemy.orm import Session
from database import get_db
from models import FoodItem
import resend
import cloudinary
import cloudinary.uploader
import os

router = APIRouter()
UPLOAD_DIR = "uploads/foods"
os.makedirs(UPLOAD_DIR, exist_ok=True)
ADMIN_EMAIL = "bottestserver002@gmail.com"

@router.get("/foods")
def get_foods(db: Session = Depends(get_db)):
    foods = db.query(FoodItem).order_by(FoodItem.name.asc()).all()

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
    image_path = None

    if image:
        file_path = f"{UPLOAD_DIR}/{image.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        image_path = f"/{file_path}"

    food = FoodItem(
        name=name,
        category=category,
        image=image_path
    )

    db.add(food)
    db.commit()
    db.refresh(food)

    return {"message": "Đã thêm món"}


@router.put("/foods/{food_id}")
def update_food(
    food_id: int,
    name: str = Form(...),
    category: str = Form(...),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    food = db.query(FoodItem).filter(FoodItem.id == food_id).first()

    if not food:
        raise HTTPException(status_code=404, detail="Không tìm thấy món")

    food.name = name
    food.category = category

    if image:
        file_path = f"{UPLOAD_DIR}/{image.filename}"

        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

        food.image = f"/{file_path}"

    db.commit()

    return {"message": "Đã cập nhật món"}

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

        return {"message": "Bạn đã oder món thành công"}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Lỗi gửi order: {str(e)}"
        )
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

@router.get("/test-cloudinary")
def test_cloudinary():

    result = cloudinary.uploader.upload(
        "https://res.cloudinary.com/demo/image/upload/sample.jpg",
        folder="booking_food"
    )

    return result["secure_url"]