from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.deps.auth import get_current_user

router = APIRouter()


@router.post("/bookings")
def create_booking(
    class_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user)
):

    class_obj = db.query(Class).filter(Class.id == class_id).first()

    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")

    booking = Booking(
        class_id=class_id,
        user_id=user["user_id"]
    )

    db.add(booking)
    db.commit()

    return booking