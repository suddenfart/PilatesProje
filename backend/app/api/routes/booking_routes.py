from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.models.user_package import UserPackage

router = APIRouter(tags=["Bookings"])


# 📦 REQUEST MODEL
class BookingCreate(BaseModel):
    user_id: int
    class_id: int


@router.post("/")
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):

    # kullanıcı package kontrol
    package = db.query(UserPackage).filter(
        UserPackage.user_id == data.user_id
    ).first()

    if not package or package.remaining_sessions <= 0:
        raise HTTPException(status_code=400, detail="No sessions left")

    # class kontrol
    class_obj = db.query(Class).filter(Class.id == data.class_id).first()

    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")

    # booking create
    booking = Booking(
        user_id=data.user_id,
        class_id=data.class_id
    )

    package.remaining_sessions -= 1

    db.add(booking)
    db.commit()
    db.refresh(booking)

    return {
        "message": "Booking created",
        "booking_id": booking.id,
        "remaining_sessions": package.remaining_sessions
    }