from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.deps import get_db
from app.models.booking import Booking
from app.models.class_model import Class
from app.models.user import User
from app.models.user_package import UserPackage

router = APIRouter(prefix="/bookings", tags=["Bookings"])


class BookingCreate(BaseModel):
    user_id: int
    class_id: int


@router.post("/")
def create_booking(data: BookingCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == data.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    class_obj = db.query(Class).filter(Class.id == data.class_id).first()
    if not class_obj:
        raise HTTPException(status_code=404, detail="Class not found")

    existing = db.query(Booking).filter(
        Booking.user_id == data.user_id,
        Booking.class_id == data.class_id
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Already booked")

    # 💳 PACKAGE CHECK
    package = db.query(UserPackage).filter(
        UserPackage.user_id == data.user_id,
        UserPackage.remaining_sessions > 0
    ).first()

    if not package:
        raise HTTPException(status_code=400, detail="No sessions left")

    # 👥 CAPACITY CHECK
    count = db.query(Booking).filter(
        Booking.class_id == data.class_id
    ).count()

    if count >= class_obj.capacity:
        raise HTTPException(status_code=400, detail="Class full")

    # 🔥 BOOK
    booking = Booking(
        user_id=data.user_id,
        class_id=data.class_id
    )

    package.remaining_sessions -= 1

    db.add(booking)
    db.add(package)
    db.commit()
    db.refresh(booking)

    return {"message": "Booked"}