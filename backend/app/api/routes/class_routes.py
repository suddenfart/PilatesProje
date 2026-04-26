from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.class_model import Class
from app.models.user import User
from app.schemas.class_schema import ClassCreate, ClassOut
from app.core.security import get_current_user

router = APIRouter(prefix="/classes", tags=["Classes"])


@router.post("/", response_model=ClassOut)
def create_class(
    data: ClassCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # ⛔️ validation: time check
    if data.start_time >= data.end_time:
        raise HTTPException(
            status_code=400,
            detail="end_time must be after start_time"
        )

    # 🧠 create class
    new_class = Class(
        start_time=data.start_time,
        end_time=data.end_time,
        capacity=data.capacity,
        teacher_id=current_user.id  # 🔥 backend assigns teacher
    )

    db.add(new_class)
    db.commit()
    db.refresh(new_class)

    return new_class