from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.class_model import Class
from app.deps.auth import get_current_user, admin_only

router = APIRouter()


@router.get("/classes")
def get_classes(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return db.query(Class).all()


@router.post("/classes")
def create_class(
    start_time: str,
    end_time: str,
    capacity: int,
    db: Session = Depends(get_db),
    admin=Depends(admin_only)
):
    new_class = Class(
        start_time=start_time,
        end_time=end_time,
        capacity=capacity,
        teacher_id=1
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class