from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Workspace

router = APIRouter()


@router.get("/workspaces")
def get_workspaces(db: Session = Depends(get_db)):
    return db.query(Workspace).all()


@router.post("/workspaces")
def create_workspace(
    data: dict,
    db: Session = Depends(get_db)
):

    workspace = Workspace(
        name=data["name"],
        description=data.get("description", ""),
        color=data.get("color", "#2563eb"),
        icon=data.get("icon", "📁"),
        user_id=data["user_id"]
    )

    db.add(workspace)

    db.commit()

    db.refresh(workspace)

    return workspace


@router.put("/workspaces/{id}")
def update_workspace(
    id: int,
    data: dict,
    db: Session = Depends(get_db)
):

    w = db.query(Workspace).filter(
        Workspace.id == id
    ).first()

    if not w:
        return {"message": "Không tìm thấy"}

    w.name = data["name"]
    w.description = data["description"]
    w.color = data["color"]
    w.icon = data["icon"]

    db.commit()

    return {"message": "OK"}


@router.delete("/workspaces/{id}")
def delete_workspace(
    id: int,
    db: Session = Depends(get_db)
):

    w = db.query(Workspace).filter(
        Workspace.id == id
    ).first()

    if not w:
        return {"message": "Không tìm thấy"}

    db.delete(w)

    db.commit()

    return {"message": "Đã xóa"}