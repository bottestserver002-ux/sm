from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from database import get_db
from models import User, Post, Poem, SiteVisit

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.post("/visit")
def record_visit(
    request: Request,
    db: Session = Depends(get_db)
):
    ip = request.client.host if request.client else None
    user_agent = request.headers.get("user-agent")

    visit = SiteVisit(
        ip=ip,
        user_agent=user_agent
    )

    db.add(visit)
    db.commit()

    return {"message": "Recorded"}


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    visits = db.query(SiteVisit).count()
    users = db.query(User).count()
    posts = db.query(Post).count()
    poems = db.query(Poem).count()

    return {
        "visits": visits,
        "contents": posts + poems,
        "users": users,
        "status": "24/7"
    }