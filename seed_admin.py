from sqlalchemy.orm import Session

from database import SessionLocal
from models import User
from auth import hash_password


ADMIN_EMAIL = "bottestserver002@gmail.com"
ADMIN_PASSWORD = "ffkid1412"


def create_admin():

    db: Session = SessionLocal()

    try:

        existing_admin = db.query(User).filter(
            User.email == ADMIN_EMAIL
        ).first()

        if existing_admin:
            print("Admin already exists")
            return

        admin = User(
            username="admin",
            email=ADMIN_EMAIL,
            password=hash_password(ADMIN_PASSWORD),
            is_admin=True
        )

        db.add(admin)
        db.commit()

        print("Admin created successfully")

    except Exception as e:
        print("Error creating admin:", e)

    finally:
        db.close()


if __name__ == "__main__":
    create_admin()