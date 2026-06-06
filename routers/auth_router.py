from pydoc import html

from schemas import RegisterSchema, LoginSchema
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session  
from datetime import datetime, timedelta
import smtplib
import random
import os

from email.mime.text import MIMEText
from models import User, OTPCode

from database import get_db
from models import User
from auth import hash_password, verify_password, create_access_token

router = APIRouter()
MAIL_USER = os.getenv("MAIL_USER")
MAIL_PASS = os.getenv("MAIL_PASS") 


@router.post("/register")
def register(data: dict,
             db: Session = Depends(get_db)):

    otp_record = db.query(OTPCode).filter(
        OTPCode.email == data["email"],
        OTPCode.otp == data["otp"]
    ).first()

    if not otp_record:

        return {
            "message": "OTP không đúng"
        }

    if otp_record.expires_at < datetime.utcnow():

        return {
            "message": "OTP đã hết hạn"
        }

    # tạo user

    user = User(
        username=data["username"],
        email=data["email"],
        password=hash_password(
            data["password"]
        )
    )

    db.add(user)

    db.commit()

    return {
        "message": "Đăng ký thành công"
    }


@router.post("/login")
def login(data: LoginSchema, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(400, "Email hoặc mật khẩu không đúng")

    token = create_access_token({
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "is_admin": user.is_admin
    })

    return {
        "token": token,
        "user": {
            "username": user.username,
            "email": user.email,
            "is_admin": user.is_admin
        }
    }
@router.get("/make-admin")
def make_admin(db: Session = Depends(get_db)):

    user = db.query(User).filter(
        User.email == "bottestserver002@gmail.com"
    ).first()

    if not user:
        return {"error": "User not found"}

    user.is_admin = True

    db.commit()

    return {"message": "Admin updated"}

@router.post("/send-otp")
def send_otp(data: dict, db: Session = Depends(get_db)):

    email = data["email"]

    otp = str(random.randint(100000, 999999))

    expire = datetime.utcnow() + timedelta(minutes=3)

    db.add(
        OTPCode(
            email=email,
            otp=otp,
            expires_at=expire
        )
    )

    db.commit()

    html = f"""
<html>
<body style="font-family: Arial, sans-serif; background:#f4f4f4; padding:20px;">

<div style="max-width:600px; margin:auto; background:white; border-radius:12px; overflow:hidden;">

    <div style="background:#2563eb; color:white; padding:20px; text-align:center;">
        <h1>Website Cá Nhân</h1>
    </div>

    <div style="padding:30px;">
        <h2>Xác thực tài khoản</h2>

        <p>Cảm ơn bạn đã đăng ký.</p>

        <p>Mã OTP của bạn là:</p>

        <div style="
            font-size:32px;
            font-weight:bold;
            letter-spacing:8px;
            text-align:center;
            background:#f3f4f6;
            padding:15px;
            border-radius:8px;
        ">
            {otp}
        </div>

        <p style="margin-top:20px;">
            Mã có hiệu lực trong <b>3 phút</b>.
        </p>
    </div>

    <div style="
        background:#f9fafb;
        padding:15px;
        text-align:center;
        color:#666;
    ">
        © 2026 Website Cá Nhân
    </div>

</div>

</body>
</html>
"""

    msg = MIMEText(html, "html", "utf-8")

    msg["Subject"] = "Mã xác nhận đăng ký"

    msg["From"] = MAIL_USER

    msg["To"] = email

    server = smtplib.SMTP(
        "smtp.gmail.com",
        587
    )

    server.starttls()

    server.login(
        MAIL_USER,
        MAIL_PASS
    )

    server.send_message(msg)

    server.quit()

    return {
        "message": "Đã gửi OTP"
    }